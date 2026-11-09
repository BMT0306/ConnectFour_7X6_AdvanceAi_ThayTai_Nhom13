"""Kiểm thử toàn diện cho mô hình Policy-Value ResNet, NNAgent, MixedMCTSAgent (PUCT) và Saliency XAI."""
from __future__ import annotations

import numpy as np
import torch

from c4.agents import Budget, MixedMCTSAgent, NNAgent
from c4.game import Connect4, ReferenceConnect4
from c4.models import Connect4PolicyValueNet, compute_saliency_map


def test_policy_value_net_shapes_and_legal_mask():
    net = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64)
    g = Connect4()
    # Làm đầy cột 0 (6 quân)
    for _ in range(6):
        g.step(0)

    x = torch.from_numpy(g.encode()).unsqueeze(0)
    logits, val = net(x)
    assert logits.shape == (1, 7)
    assert val.shape == (1, 1)
    assert -1.0 <= float(val.item()) <= 1.0

    mask = np.array([[c in g.legal_actions() for c in range(7)]], dtype=bool)
    probs = net.predict_action_probs(x, legal_mask=mask, temperature=1.0).squeeze(0).numpy()
    assert probs[0] == 0.0, "Cột đã đầy bắt buộc có xác suất = 0"
    assert abs(float(probs.sum()) - 1.0) < 1e-5


def test_nn_agent_legality_and_temperature():
    g = Connect4()
    for _ in range(6):
        g.step(3)  # làm đầy cột giữa

    agent_det = NNAgent(seed=7, temperature=0.0)
    c1 = agent_det.choose_action(g)
    c2 = agent_det.choose_action(g)
    assert c1 == c2 and c1 != 3 and c1 in g.legal_actions()

    agent_stoch = NNAgent(seed=7, temperature=1.2)
    c3 = agent_stoch.choose_action(g)
    assert c3 != 3 and c3 in g.legal_actions()


def test_mixed_mcts_dirichlet_noise_and_reference_engine_compatibility():
    """Kiểm chứng sửa lỗi Dirichlet noise (gammavariate), bất biến cache và tương thích ReferenceConnect4."""
    agent = MixedMCTSAgent(
        seed=42,
        default_simulations=24,
        use_value_head=True,
        add_dirichlet_noise=True,
        dirichlet_alpha=0.3,
        dirichlet_epsilon=0.25,
    )

    for EngineCls in (Connect4, ReferenceConnect4):
        g = EngineCls()
        g.step(3)
        g.step(2)
        col = agent.choose_action(g, Budget(simulations=24))
        assert col in g.legal_actions()
        assert agent.last_stats["simulations"] == 24
        # Kiểm tra xác suất lưu trong cache vẫn chuẩn hóa = 1 và không âm
        for probs, val in agent._cache.values():
            assert np.all(probs >= 0.0)
            assert abs(float(probs.sum()) - 1.0) < 1e-4
            assert -1.0 <= val <= 1.0


def test_mixed_mcts_rollout_mode_finds_immediate_win():
    """Kiểm tra chế độ use_value_head=False (phục vụ Ablation A3) nhận diện nước thắng ngay."""
    g = Connect4()
    # X có 3 quân hàng đáy ở cột 0, 1, 2; O có 3 quân ở cột 6 (nhưng đến lượt X thắng ngay ở cột 3)
    for m in (0, 6, 1, 6, 2, 6):
        g.step(m)

    agent = MixedMCTSAgent(seed=10, default_simulations=60, use_value_head=False)
    move = agent.choose_action(g, Budget(simulations=60))
    assert move == 3


def test_xai_saliency_map_output():
    net = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64)
    g = Connect4()
    for m in (3, 0, 4, 0, 5):  # đòn kép hàng đáy
        g.step(m)

    out = compute_saliency_map(net, g)
    sal = out["saliency"]
    assert sal.shape == (6, 7)
    assert float(sal.min()) >= 0.0
    assert float(sal.max()) <= 1.0 + 1e-6
    assert out["chosen_col"] in g.legal_actions()
    assert out["probs"].shape == (7,)


def test_trained_checkpoint_tactical_sanity():
    """Khi đã có checkpoint huấn luyện, NNAgent và MixedMCTSAgent phải nạp thành công và xử lý đòn chiến thuật cơ bản."""
    nn_agent = NNAgent(seed=42, temperature=0.0)
    puct_agent = MixedMCTSAgent(seed=42, default_simulations=80, use_value_head=True)
    if not nn_agent.has_checkpoint:
        return  # Cho phép chạy test độc lập trên môi trường CI sạch chưa huấn luyện

    assert puct_agent.has_checkpoint is True

    # 1. Nước thắng trực tiếp hàng ngang chuẩn (X có 0, 1, 2 -> đánh 3 thắng ngay)
    g_win = Connect4()
    for m in (0, 5, 1, 6, 2, 5):
        g_win.step(m)
    assert nn_agent.choose_action(g_win) == 3
    assert puct_agent.choose_action(g_win, Budget(simulations=80)) == 3
    assert nn_agent.last_stats["has_checkpoint"] is True
    assert puct_agent.last_stats["has_checkpoint"] is True

    # 2. Nước chặn thua trực tiếp (X có 0, 1, 2 -> lượt O bắt buộc chặn 3)
    g_block = Connect4()
    for m in (0, 6, 1, 5, 2):
        g_block.step(m)
    assert nn_agent.choose_action(g_block) == 3
    assert puct_agent.choose_action(g_block, Budget(simulations=80)) == 3

    # 3. Thế cờ đồng thời cả hai bên có chuỗi 3 quân: PUCT tìm kiếm cây phải ưu tiên thắng ngay ở cột 3
    g_simul = Connect4()
    for m in (0, 6, 1, 6, 2, 6):
        g_simul.step(m)
    assert puct_agent.choose_action(g_simul, Budget(simulations=100)) == 3


