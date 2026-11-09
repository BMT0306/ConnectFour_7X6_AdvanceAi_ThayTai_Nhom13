"""Explainable AI (XAI) cho mô hình Connect4PolicyValueNet.

Trích xuất bản đồ nhiệt độ nhạy Gradient (Input Saliency Heatmap):
    G(r, c) = sum_{k in {0, 1}} | d logit(a*) / d X[k, r, c] |
nhằm minh bạch hóa vùng không gian bàn cờ (cột trung tâm, chuỗi 3 quân, thế đòn kép)
mà mạng nơ-ron tập trung chú ý khi đưa ra quyết định.
"""
from __future__ import annotations

import numpy as np
import torch

from c4.game.base import Connect4Base
from c4.models.model import Connect4PolicyValueNet


def compute_saliency_map(
    model: Connect4PolicyValueNet,
    game: Connect4Base,
    target_col: int | None = None,
    device: torch.device | str | None = None,
) -> dict[str, np.ndarray | float | int]:
    """Tính Saliency Map (6, 7) đã chuẩn hóa [0, 1] cho trạng thái bàn cờ `game`.

    Nếu `target_col` là None, hàm tự động lấy cột hợp lệ có xác suất dự đoán cao nhất `a*`.
    """
    if device is None:
        dev = next(model.parameters()).device
    else:
        dev = torch.device(device)

    model.eval()
    model.zero_grad(set_to_none=True)

    legal = game.legal_actions()
    if not legal:
        raise ValueError("Không thể trích xuất Saliency Map trên bàn cờ không còn nước đi hợp lệ.")

    state_np = game.encode()  # (2, 6, 7)
    x = torch.tensor(state_np, dtype=torch.float32, device=dev).unsqueeze(0)
    x.requires_grad_(True)

    logits, value_t = model(x)

    mask = torch.zeros((1, 7), dtype=torch.bool, device=dev)
    for c in legal:
        mask[0, c] = True
    masked_logits = torch.where(mask, logits, torch.full_like(logits, -1e9))
    probs_t = torch.softmax(masked_logits, dim=-1)

    chosen_col = int(torch.argmax(masked_logits[0]).item()) if target_col is None else int(target_col)
    score_target = logits[0, chosen_col]
    score_target.backward()

    grad = x.grad.detach().abs().squeeze(0).cpu().numpy()  # (2, 6, 7)
    saliency = grad.sum(axis=0)  # Gộp độ nhạy trên cả kênh quân ta và quân đối thủ -> (6, 7)

    s_max = float(saliency.max())
    if s_max > 1e-12:
        saliency_norm = (saliency / s_max).astype(np.float32)
    else:
        saliency_norm = np.zeros_like(saliency, dtype=np.float32)

    return {
        "saliency": saliency_norm,
        "raw_saliency": saliency.astype(np.float32),
        "probs": probs_t.detach().squeeze(0).cpu().numpy().astype(np.float32),
        "value": float(value_t.detach().squeeze().item()),
        "chosen_col": chosen_col,
    }

