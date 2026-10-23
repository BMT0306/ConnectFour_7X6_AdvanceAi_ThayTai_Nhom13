"""Huấn luyện mô hình mạng nơ-ron Connect4PolicyValueNet bằng PyTorch.

Quy trình:
1. Đọc dữ liệu từ file npz (train, val, test) do gen_data.py tạo.
2. Huấn luyện bằng AdamW kết hợp học phân phối Policy (CrossEntropyLoss) và Value (MSELoss).
3. Đánh giá độ chính xác (Top-1 Accuracy) và Loss sau mỗi epoch.
4. Tự động lưu checkpoint tốt nhất vào checkpoints/policy_net_best.pt.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from c4.models.model import Connect4PolicyValueNet


class Connect4Dataset(Dataset):
    """Dataset quản lý các mẫu bàn cờ Connect Four."""

    def __init__(self, npz_path: str | Path) -> None:
        data = np.load(npz_path)
        self.states = torch.from_numpy(data["states"]).float()  # (N, 2, 6, 7)
        self.actions = torch.from_numpy(data["actions"]).long()  # (N,)
        self.legal_masks = torch.from_numpy(data["legal_masks"]).bool()  # (N, 7)
        self.values = torch.from_numpy(data["values"]).float().unsqueeze(1)  # (N, 1)

    def __len__(self) -> int:
        return len(self.actions)

    def __getitem__(self, idx: int):
        return self.states[idx], self.actions[idx], self.legal_masks[idx], self.values[idx]


def evaluate(
    model: nn.Module,
    dataloader: DataLoader,
    device: torch.device,
    policy_criterion: nn.Module,
    value_criterion: nn.Module,
) -> tuple[float, float, float]:
    """Đánh giá mô hình trên tập validation hoặc test."""
    model.eval()
    total_loss = 0.0
    correct_actions = 0
    total_samples = 0

    with torch.no_grad():
        for states, actions, masks, values in dataloader:
            states = states.to(device)
            actions = actions.to(device)
            masks = masks.to(device)
            values = values.to(device)

            policy_logits, value_preds = model(states)

            # Policy loss
            p_loss = policy_criterion(policy_logits, actions)
            # Value loss
            v_loss = value_criterion(value_preds, values)
            loss = p_loss + 0.5 * v_loss

            total_loss += loss.item() * len(actions)

            # Tính độ chính xác có xét mask
            masked_logits = torch.where(masks, policy_logits, torch.tensor(-1e9, device=device))
            preds = torch.argmax(masked_logits, dim=-1)
            correct_actions += (preds == actions).sum().item()
            total_samples += len(actions)

    avg_loss = total_loss / max(total_samples, 1)
    acc = correct_actions / max(total_samples, 1)
    return avg_loss, acc, correct_actions


def train_policy_net(
    data_dir: str | Path = "data",
    checkpoint_dir: str | Path = "checkpoints",
    epochs: int = 15,
    batch_size: int = 64,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    device_str: str | None = None,
) -> Path:
    data_path = Path(data_dir)
    ckpt_path = Path(checkpoint_dir)
    ckpt_path.mkdir(parents=True, exist_ok=True)

    train_file = data_path / "train.npz"
    val_file = data_path / "val.npz"

    if not train_file.exists() or not val_file.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu tại {data_path}. Hãy chạy gen_data.py trước!")

    if device_str is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_str)

    print(f"[*] Huấn luyện mạng Connect4PolicyValueNet trên thiết bị: {device}")

    train_dataset = Connect4Dataset(train_file)
    val_dataset = Connect4Dataset(val_file)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    print(f"[*] Tập Train: {len(train_dataset)} mẫu | Tập Val: {len(val_dataset)} mẫu")

    model = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

    policy_criterion = nn.CrossEntropyLoss()
    value_criterion = nn.MSELoss()

    best_val_loss = float("inf")
    best_ckpt_file = ckpt_path / "policy_net_best.pt"
    history = []

    start_train = time.perf_counter()

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        train_correct = 0
        total_train = 0

        for states, actions, masks, values in train_loader:
            states = states.to(device)
            actions = actions.to(device)
            masks = masks.to(device)
            values = values.to(device)

            optimizer.zero_grad()
            policy_logits, value_preds = model(states)

            p_loss = policy_criterion(policy_logits, actions)
            v_loss = value_criterion(value_preds, values)
            loss = p_loss + 0.5 * v_loss

            loss.backward()
            optimizer.step()

            train_loss += loss.item() * len(actions)
            with torch.no_grad():
                masked_logits = torch.where(masks, policy_logits, torch.tensor(-1e9, device=device))
                preds = torch.argmax(masked_logits, dim=-1)
                train_correct += (preds == actions).sum().item()
                total_train += len(actions)

        epoch_tr_loss = train_loss / max(total_train, 1)
        epoch_tr_acc = train_correct / max(total_train, 1)

        val_loss, val_acc, _ = evaluate(model, val_loader, device, policy_criterion, value_criterion)
        scheduler.step(val_loss)

        is_best = val_loss < best_val_loss
        if is_best:
            best_val_loss = val_loss
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_loss": val_loss,
                "val_acc": val_acc,
                "config": {"num_res_blocks": 3, "num_filters": 64},
            }, best_ckpt_file)

        print(
            f"Epoch {epoch:02d}/{epochs:02d} | "
            f"Train Loss: {epoch_tr_loss:.4f} Acc: {epoch_tr_acc * 100:.2f}% | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc * 100:.2f}% "
            f"{'(*Best*)' if is_best else ''}"
        )

        history.append({
            "epoch": epoch,
            "train_loss": epoch_tr_loss,
            "train_acc": epoch_tr_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
        })

    total_time = time.perf_counter() - start_train
    print(f"\n[+] Huấn luyện xong trong {total_time:.1f}s!")
    print(f"[+] Checkpoint tốt nhất đã lưu tại: {best_ckpt_file} (Val Loss: {best_val_loss:.4f})")

    # Lưu lịch sử huấn luyện
    with open(ckpt_path / "training_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    return best_ckpt_file


def main():
    p = argparse.ArgumentParser(description="Huấn luyện mô hình CNN Connect Four")
    p.add_argument("--data-dir", default="data")
    p.add_argument("--checkpoint-dir", default="checkpoints")
    p.add_argument("--epochs", type=int, default=12)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--lr", type=float, default=1e-3)
    args = p.parse_args()

    train_policy_net(
        data_dir=args.data_dir,
        checkpoint_dir=args.checkpoint_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
    )


if __name__ == "__main__":
    main()
