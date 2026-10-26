"""Cấp mở rộng - MixedMCTSAgent: Kết hợp MCTS với xác suất tiên nghiệm (Prior) từ Policy Network (PUCT).

Theo công thức AlphaZero/PUCT:
    PUCT(s, a) = Q(s, a) + c_puct * P(s, a) * (sqrt(N_cha) / (1 + N_con))

Trong đó:
- Q(s, a) = W / N: Giá trị khai thác trung bình
- P(s, a): Xác suất tiên nghiệm do mạng CNN dự đoán
- N_cha, N_con: Số lần thăm nút cha và nút con
- c_puct: Hằng số điều chỉnh mức độ khám phá
"""
from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
import torch

from c4.agents.base import Agent, Budget
from c4.game.base import Connect4Base
from c4.models.model import Connect4PolicyValueNet

DEFAULT_CKPT = Path(__file__).resolve().parent.parent.parent.parent / "checkpoints" / "policy_net_best.pt"


class _PUCTNode:
    __slots__ = ("move", "parent", "mover", "children", "untried", "N", "W", "prior_p")

    def __init__(self, move, parent, mover, untried, prior_p: float = 1.0):
        self.move = move
        self.parent = parent
        self.mover = mover
        self.children: list[_PUCTNode] = []
        self.untried = untried
        self.N = 0
        self.W = 0.0
        self.prior_p = prior_p


class MixedMCTSAgent(Agent):
    name = "mixed_mcts"

    def __init__(
        self,
        seed: int | None = None,
        default_simulations: int = 500,
        c_puct: float = 2.0,
        use_value_head: bool = True,
        checkpoint_path: str | Path | None = None,
        device: str | None = None,
    ) -> None:
        super().__init__(seed)
        self.default_simulations = default_simulations
        self.c_puct = c_puct
        self.use_value_head = use_value_head
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))

        # Bộ nhớ đệm chuyển vị (Transposition Cache)
        self._cache: dict[tuple, tuple[np.ndarray, float]] = {}

        # Mô hình nơ-ron
        self.model = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64).to(self.device)
        self.model.eval()

        ckpt = Path(checkpoint_path) if checkpoint_path else DEFAULT_CKPT
        if ckpt.exists():
            try:
                data = torch.load(ckpt, map_location=self.device)
                state_dict = data["model_state_dict"] if "model_state_dict" in data else data
                self.model.load_state_dict(state_dict)
            except Exception:
                pass

    def _state_key(self, g: Connect4Base) -> tuple:
        """Tạo khóa băm cho bàn cờ để tra cứu trong bộ nhớ đệm."""
        if hasattr(g, "_pos") and hasattr(g, "_mask"):
            return (g.current_player, g._pos, g._mask)
        return (g.current_player, tuple(g.board.flatten()))

    def _get_priors(self, g: Connect4Base) -> tuple[np.ndarray, float]:
        """Dự đoán prior probabilities và value từ CNN có sử dụng bộ nhớ đệm."""
        key = self._state_key(g)
        if key in self._cache:
            return self._cache[key]

        legal = g.legal_actions()
        if not legal:
            return np.ones(7) / 7.0, 0.0

        state_np = g.encode()
        state_t = torch.from_numpy(state_np).unsqueeze(0).to(self.device)
        mask = np.zeros(7, dtype=bool)
        for c in legal:
            mask[c] = True
        mask_t = torch.from_numpy(mask).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits, val_t = self.model(state_t)
            masked_logits = torch.where(mask_t, logits, torch.tensor(-1e9, device=self.device))
            probs = torch.softmax(masked_logits, dim=-1).cpu().numpy().squeeze(0)
            val = float(val_t.squeeze().item())

        res = (probs, val)
        self._cache[key] = res
        return res

    def _select_child(self, node: _PUCTNode) -> _PUCTNode:
        sqrt_parent_n = math.sqrt(max(node.N, 1))
        c_puct = self.c_puct
        best, best_score = None, -1e9

        for ch in node.children:
            q = (ch.W / ch.N) if ch.N > 0 else 0.5
            u = c_puct * ch.prior_p * (sqrt_parent_n / (1.0 + ch.N))
            score = q + u
            if score > best_score:
                best, best_score = ch, score
        return best

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        legal = game.legal_actions()
        if len(legal) == 1:
            self.last_stats = {"simulations": 0}
            return legal[0]

        # Reset cache mỗi nước đi để tiết kiệm bộ nhớ
        self._cache.clear()

        max_sims = budget.simulations if budget and budget.simulations else None
        time_s = budget.time_s if budget else None
        if max_sims is None and time_s is None:
            max_sims = self.default_simulations
        deadline = time.perf_counter() + time_s if time_s is not None else None

        # Khởi tạo gốc với priors
        root_priors, _ = self._get_priors(game)
        root = _PUCTNode(None, None, -game.current_player, list(legal))

        sims = 0
        cache_hits = 0
        while max_sims is None or sims < max_sims:
            if deadline is not None and sims > 0 and (sims & 7) == 0 and time.perf_counter() > deadline:
                break

            g = game.clone()
            node = root

            # 1. Selection
            while not node.untried and node.children:
                node = self._select_child(node)
                g.step(node.move)

            # 2. Expansion
            if node.untried and not g.is_terminal():
                priors, val_leaf = self._get_priors(g)
                # Lấy nước đi có prior cao nhất trong số untried
                mv = max(node.untried, key=lambda m: priors[m])
                node.untried.remove(mv)
                mover = g.current_player
                g.step(mv)
                child = _PUCTNode(
                    mv,
                    node,
                    mover,
                    [] if g.is_terminal() else g.legal_actions(),
                    prior_p=float(priors[mv]),
                )
                node.children.append(child)
                node = child

            # 3. Evaluation (Value Head vs Rollout)
            if self.use_value_head:
                if g.is_terminal():
                    w = g.winner
                    # Giá trị theo góc nhìn của người chơi node.mover
                    if w == 0:
                        v_eval = 0.0
                    else:
                        v_eval = 1.0 if node.mover == w else -1.0
                else:
                    _, val_net = self._get_priors(g)
                    # val_net là lượng giá theo góc nhìn của g.current_player (đối thủ của node.mover)
                    # Do đó với node.mover thì giá trị thế cờ là -val_net
                    v_eval = -val_net

                # 4. Backpropagation (Value Head mode)
                # Chuyển v_eval [-1, 1] về xác suất thắng [0, 1] cho node.mover
                win_prob_mover = (v_eval + 1.0) / 2.0
                curr = node
                while curr is not None:
                    curr.N += 1
                    if curr.mover == node.mover:
                        curr.W += win_prob_mover
                    else:
                        curr.W += (1.0 - win_prob_mover)
                    curr = curr.parent
            else:
                # Chế độ Rollout ngẫu nhiên truyền thống (dùng cho Ablation A3)
                while not g.is_terminal():
                    wins = g.winning_moves()
                    g.step(self.rng.choice(wins) if wins else self.rng.choice(g.legal_actions()))

                w = g.winner
                curr = node
                while curr is not None:
                    curr.N += 1
                    curr.W += 1.0 if curr.mover == w else (0.5 if w == 0 else 0.0)
                    curr = curr.parent

            sims += 1

        best = max(root.children, key=lambda ch: (ch.N, ch.W / max(ch.N, 1)))
        self.last_stats = {
            "simulations": sims,
            "best_visits": best.N,
            "best_winrate": round(best.W / max(best.N, 1), 3),
            "use_value_head": self.use_value_head,
        }
        return best.move


# Alias chuẩn AlphaZero
PUCTAgent = MixedMCTSAgent
AlphaZeroAgent = MixedMCTSAgent

