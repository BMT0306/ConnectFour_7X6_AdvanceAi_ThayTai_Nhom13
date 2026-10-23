"""Mô hình mạng nơ-ron tích chập (CNN) cho Connect Four.

Đầu vào: Tensor shape (B, 2, 6, 7)
- Kênh 0: Vị trí các quân của bên đang đến lượt (+1)
- Kênh 1: Vị trí các quân của đối thủ (-1)

Đầu ra:
- Policy logits (B, 7): Điểm số cho 7 cột hành động (kèm legal move mask)
- Value (B, 1): Ước lượng xác suất thắng / giá trị trạng thái [-1, 1]
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class ConvBlock(nn.Module):
    """Khối tích chập với Batch Normalization và ReLU."""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, padding: int = 1) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, padding=padding, bias=False)
        self.bn = nn.BatchNorm2d(out_channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.relu(self.bn(self.conv(x)))


class ResidualBlock(nn.Module):
    """Khối phần dư (Residual Block) giúp huấn luyện mạng sâu ổn định."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return F.relu(out)


class Connect4PolicyValueNet(nn.Module):
    """Mạng CNN sâu dự đoán phân phối Policy (7 cột) và Value (trạng thái bàn cờ)."""

    def __init__(self, num_res_blocks: int = 3, num_filters: int = 64) -> None:
        super().__init__()
        # Input layer: 2 kênh (ta, đối thủ)
        self.in_conv = ConvBlock(2, num_filters, kernel_size=3, padding=1)

        # Residual backbone
        self.res_blocks = nn.ModuleList([ResidualBlock(num_filters) for _ in range(num_res_blocks)])

        # Policy head: Conv 1x1 -> Flatten -> Dense -> 7 logits
        self.policy_conv = nn.Conv2d(num_filters, 32, kernel_size=1, bias=False)
        self.policy_bn = nn.BatchNorm2d(32)
        self.policy_fc = nn.Linear(32 * 6 * 7, 7)

        # Value head: Conv 1x1 -> Flatten -> Dense(64) -> Dense(1) -> Tanh [-1, 1]
        self.value_conv = nn.Conv2d(num_filters, 16, kernel_size=1, bias=False)
        self.value_bn = nn.BatchNorm2d(16)
        self.value_fc1 = nn.Linear(16 * 6 * 7, 64)
        self.value_fc2 = nn.Linear(64, 1)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Trả về (policy_logits, value).

        x: shape (B, 2, 6, 7)
        policy_logits: shape (B, 7)
        value: shape (B, 1) trong khoảng [-1, 1]
        """
        out = self.in_conv(x)
        for block in self.res_blocks:
            out = block(out)

        # Policy head
        p = F.relu(self.policy_bn(self.policy_conv(out)))
        p = p.flatten(start_dim=1)
        policy_logits = self.policy_fc(p)

        # Value head
        v = F.relu(self.value_bn(self.value_conv(out)))
        v = v.flatten(start_dim=1)
        v = F.relu(self.value_fc1(v))
        value = torch.tanh(self.value_fc2(v))

        return policy_logits, value

    def predict_action_probs(
        self,
        x: torch.Tensor,
        legal_mask: torch.Tensor | np.ndarray | None = None,
        temperature: float = 1.0,
    ) -> torch.Tensor:
        """Tính phân phối xác suất softmax trên các nước đi hợp lệ.

        Nước đi bất hợp lệ được gán xác suất = 0 bằng cách gán logit = -1e9 trước softmax.
        """
        self.eval()
        with torch.no_grad():
            logits, _ = self.forward(x)

            if legal_mask is not None:
                if isinstance(legal_mask, np.ndarray):
                    legal_mask = torch.from_numpy(legal_mask).to(logits.device)
                # Gán -inf (hoặc -1e9) vào các ô không hợp lệ
                mask_bool = legal_mask.bool()
                logits = torch.where(mask_bool, logits, torch.tensor(-1e9, device=logits.device, dtype=logits.dtype))

            if temperature <= 0.0 or temperature < 1e-4:
                # Argmax deterministic one-hot
                best_idx = torch.argmax(logits, dim=-1, keepdim=True)
                probs = torch.zeros_like(logits).scatter_(-1, best_idx, 1.0)
            else:
                probs = F.softmax(logits / temperature, dim=-1)

            return probs


# Alias ngắn gọn
Connect4Net = Connect4PolicyValueNet
