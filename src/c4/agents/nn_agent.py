"""Cấp 5 - NNAgent: Tác tử sử dụng mạng nơ-ron học sâu tích chập (CNN).

Mô hình nhận trạng thái bàn cờ dạng tensor (2, 6, 7) được mã hóa tương đối,
dự đoán phân phối xác suất trên 7 cột, lọc qua legal action mask,
và chọn nước đi tối ưu nhất trong thời gian tính toán siêu tốc (vài ms).
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Sequence

import numpy as np
import torch

from c4.agents.base import Agent, Budget
from c4.game.base import Connect4Base
from c4.models.model import Connect4PolicyValueNet

DEFAULT_CKPT = Path(__file__).resolve().parent.parent.parent.parent / "checkpoints" / "policy_net_best.pt"


class NNAgent(Agent):
    name = "nn"

    def __init__(
        self,
        seed: int | None = None,
        checkpoint_path: str | Path | None = None,
        temperature: float = 0.0,
        device: str | None = None,
    ) -> None:
        super().__init__(seed)
        self.temperature = temperature
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))

        # Khởi tạo mô hình
        self.model = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64).to(self.device)
        self.model.eval()

        # Nạp weights từ checkpoint nếu có
        ckpt = Path(checkpoint_path) if checkpoint_path else DEFAULT_CKPT
        self.has_checkpoint = False

        if ckpt.exists():
            try:
                data = torch.load(ckpt, map_location=self.device)
                state_dict = data["model_state_dict"] if "model_state_dict" in data else data
                self.model.load_state_dict(state_dict)
                self.has_checkpoint = True
            except Exception as e:
                # Nếu file lỗi, giữ mô hình khởi tạo mặc định
                pass

    def choose_action(self, game: Connect4Base, budget: Budget | None = None) -> int:
        start_t = time.perf_counter()
        legal = game.legal_actions()
        if len(legal) == 1:
            self.last_stats = {"value": 0.0, "chosen": legal[0], "time_ms": 0.0}
            return legal[0]

        # 1. Chuẩn bị tensor input (1, 2, 6, 7)
        state_np = game.encode()  # relative encoding: shape (2, 6, 7)
        state_t = torch.from_numpy(state_np).unsqueeze(0).to(self.device)

        # 2. Tạo legal mask
        mask = np.zeros(7, dtype=bool)
        for c in legal:
            mask[c] = True

        # 3. Dự đoán policy và value
        with torch.no_grad():
            policy_logits, value_t = self.model(state_t)
            val = float(value_t.squeeze().item())

            # Mask các cột không hợp lệ bằng -1e9
            mask_t = torch.from_numpy(mask).unsqueeze(0).to(self.device)
            masked_logits = torch.where(mask_t, policy_logits, torch.tensor(-1e9, device=self.device))

            if self.temperature <= 1e-4:
                chosen = int(torch.argmax(masked_logits, dim=-1).item())
            else:
                probs = torch.softmax(masked_logits / self.temperature, dim=-1).cpu().numpy().squeeze(0)
                # Đảm bảo phân phối tổng = 1 trên legal actions
                probs_legal = np.array([probs[c] for c in legal], dtype=np.float64)
                s = probs_legal.sum()
                if s > 0:
                    probs_legal /= s
                    chosen = self.rng.choices(legal, weights=probs_legal, k=1)[0]
                else:
                    chosen = self.rng.choice(legal)

        # Kiểm tra tính an toàn: nước đi bắt buộc phải nằm trong legal actions
        if chosen not in legal:
            chosen = self.rng.choice(legal)

        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        self.last_stats = {
            "value": round(val, 3),
            "chosen": chosen,
            "time_ms": round(elapsed_ms, 2),
            "has_checkpoint": self.has_checkpoint,
        }
        return chosen
