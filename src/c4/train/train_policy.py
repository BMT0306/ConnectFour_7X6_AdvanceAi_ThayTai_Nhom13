"""Huấn luyện mô hình mạng nơ-ron hai đầu Connect4PolicyValueNet bằng PyTorch.

Quy trình chuẩn học thuật:
1. Cố định toàn bộ seed ngẫu nhiên (`random`, `numpy`, `torch`) để tái lập 100%.
2. Đọc dữ liệu từ các tập đã tách theo ván & loại trùng (`train.npz`, `val.npz`, `test.npz`).
3. Huấn luyện đa mục tiêu với AdamW:
      L = CrossEntropy(policy_logits, expert_action) + 0.5 * MSE(value_pred, game_outcome)
4. Theo dõi Top-1 Accuracy, Top-2 Accuracy, Policy Loss, Value MSE/MAE sau mỗi epoch; lưu checkpoint tốt nhất.
5. Đánh giá độc lập checkpoint tốt nhất trên tập `test.npz` (held-out test set), đo độ trễ suy luận CPU,
   xuất `checkpoints/training_history.json` và biểu đồ đường cong học tập `results/figures/nn_learning_curves.png`.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import random
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "c4_mpl_cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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


def set_global_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


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
) -> dict[str, float]:
    """Đánh giá mô hình chi tiết trên tập validation hoặc test."""
    model.eval()
    total_loss = 0.0
    total_p_loss = 0.0
    total_v_loss = 0.0
    total_v_mae = 0.0
    correct_top1 = 0
    correct_top2 = 0
    total_samples = 0

    with torch.no_grad():
        for states, actions, masks, values in dataloader:
            states = states.to(device)
            actions = actions.to(device)
            masks = masks.to(device)
            values = values.to(device)

            policy_logits, value_preds = model(states)

            p_loss = policy_criterion(policy_logits, actions)
            v_loss = value_criterion(value_preds, values)
            loss = p_loss + 0.5 * v_loss

            bs = len(actions)
            total_loss += loss.item() * bs
            total_p_loss += p_loss.item() * bs
            total_v_loss += v_loss.item() * bs
            total_v_mae += torch.abs(value_preds - values).sum().item()

            masked_logits = torch.where(masks, policy_logits, torch.full_like(policy_logits, -1e9))
            preds_top1 = torch.argmax(masked_logits, dim=-1)
            correct_top1 += (preds_top1 == actions).sum().item()

            k = min(2, masked_logits.size(-1))
            top2_indices = torch.topk(masked_logits, k=k, dim=-1).indices
            correct_top2 += (top2_indices == actions.unsqueeze(-1)).any(dim=-1).sum().item()

            total_samples += bs

    denom = max(total_samples, 1)
    return {
        "loss": total_loss / denom,
        "policy_loss": total_p_loss / denom,
        "value_mse": total_v_loss / denom,
        "value_mae": total_v_mae / denom,
        "acc": correct_top1 / denom,
        "top2_acc": correct_top2 / denom,
        "samples": total_samples,
    }


def _plot_learning_curves(history: list[dict], test_metrics: dict | None, fig_path: Path) -> None:
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    epochs = [h["epoch"] for h in history]
    tr_loss = [h["train_loss"] for h in history]
    va_loss = [h["val_loss"] for h in history]
    tr_acc = [h["train_acc"] * 100.0 for h in history]
    va_acc = [h["val_acc"] * 100.0 for h in history]
    va_top2 = [h["val_top2_acc"] * 100.0 for h in history]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

    ax1.plot(epochs, tr_loss, marker="o", linewidth=2, color="#2563EB", label="Train Joint Loss")
    ax1.plot(epochs, va_loss, marker="s", linewidth=2, color="#DC2626", label="Val Joint Loss")
    if test_metrics:
        ax1.axhline(
            test_metrics["loss"],
            linestyle="--",
            color="#059669",
            linewidth=1.6,
            label=f"Test Loss ({test_metrics['loss']:.3f})",
        )
    ax1.set_title("Hội tụ Hàm mất mát Đa mục tiêu (Policy + 0.5·Value)")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Joint Loss")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend()

    ax2.plot(epochs, tr_acc, marker="o", linewidth=2, color="#2563EB", label="Train Top-1 Acc")
    ax2.plot(epochs, va_acc, marker="s", linewidth=2, color="#DC2626", label="Val Top-1 Acc")
    ax2.plot(epochs, va_top2, marker="^", linewidth=1.8, linestyle="-.", color="#D97706", label="Val Top-2 Acc")
    if test_metrics:
        ax2.axhline(
            test_metrics["acc"] * 100.0,
            linestyle="--",
            color="#059669",
            linewidth=1.6,
            label=f"Test Top-1 Acc ({test_metrics['acc']*100:.1f}%)",
        )
    ax2.set_title("Độ chính xác Dự đoán Nước đi Chuyên gia (%)")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy (%)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close(fig)


def train_policy_net(
    data_dir: str | Path = "data",
    checkpoint_dir: str | Path = "checkpoints",
    figures_dir: str | Path = "results/figures",
    epochs: int = 10,
    batch_size: int = 256,
    lr: float = 1.5e-3,
    weight_decay: float = 1e-3,
    label_smoothing: float = 0.05,
    seed: int = 42,
    device_str: str | None = None,
) -> Path:
    set_global_seed(seed)

    data_path = Path(data_dir)
    ckpt_path = Path(checkpoint_dir)
    ckpt_path.mkdir(parents=True, exist_ok=True)

    train_file = data_path / "train.npz"
    val_file = data_path / "val.npz"
    test_file = data_path / "test.npz"

    if not train_file.exists() or not val_file.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu tại {data_path}. Hãy chạy gen_data.py trước!")

    if device_str is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_str)

    print(f"[*] Huấn luyện mạng Connect4PolicyValueNet trên thiết bị: {device} (seed={seed})")

    train_dataset = Connect4Dataset(train_file)
    val_dataset = Connect4Dataset(val_file)
    test_dataset = Connect4Dataset(test_file) if test_file.exists() else None

    g_loader = torch.Generator()
    g_loader.manual_seed(seed)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, generator=g_loader)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False) if test_dataset else None

    print(
        f"[*] Tập Train: {len(train_dataset)} mẫu | Tập Val: {len(val_dataset)} mẫu"
        + (f" | Tập Test: {len(test_dataset)} mẫu" if test_dataset else "")
    )

    model = Connect4PolicyValueNet(num_res_blocks=3, num_filters=64).to(device)
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[*] Tổng số tham số khả huấn luyện: {num_params:,}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(epochs, 1), eta_min=lr * 0.05)

    policy_criterion = nn.CrossEntropyLoss(label_smoothing=label_smoothing)
    eval_policy_criterion = nn.CrossEntropyLoss()
    value_criterion = nn.MSELoss()

    best_val_loss = float("inf")
    best_epoch = 0
    best_ckpt_file = ckpt_path / "policy_net_best.pt"
    history: list[dict] = []

    start_train = time.perf_counter()

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        train_p_loss = 0.0
        train_v_loss = 0.0
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

            bs = len(actions)
            train_loss += loss.item() * bs
            train_p_loss += p_loss.item() * bs
            train_v_loss += v_loss.item() * bs
            with torch.no_grad():
                masked_logits = torch.where(masks, policy_logits, torch.full_like(policy_logits, -1e9))
                preds = torch.argmax(masked_logits, dim=-1)
                train_correct += (preds == actions).sum().item()
                total_train += bs

        scheduler.step()

        denom = max(total_train, 1)
        epoch_tr_loss = train_loss / denom
        epoch_tr_p_loss = train_p_loss / denom
        epoch_tr_v_loss = train_v_loss / denom
        epoch_tr_acc = train_correct / denom

        val_m = evaluate(model, val_loader, device, eval_policy_criterion, value_criterion)
        val_loss = val_m["loss"]
        val_acc = val_m["acc"]

        is_best = val_loss < best_val_loss
        if is_best:
            best_val_loss = val_loss
            best_epoch = epoch
            torch.save(
                {
                    "epoch": epoch,
                    "seed": seed,
                    "model_state_dict": model.state_dict(),
                    "val_loss": val_loss,
                    "val_acc": val_acc,
                    "val_top2_acc": val_m["top2_acc"],
                    "config": {"num_res_blocks": 3, "num_filters": 64},
                },
                best_ckpt_file,
            )

        print(
            f"Epoch {epoch:02d}/{epochs:02d} | "
            f"Train Loss: {epoch_tr_loss:.4f} (P:{epoch_tr_p_loss:.4f} V:{epoch_tr_v_loss:.4f}) Acc: {epoch_tr_acc * 100:.2f}% | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc * 100:.2f}% Top2: {val_m['top2_acc'] * 100:.2f}% "
            f"{'(*Best*)' if is_best else ''}"
        )

        history.append(
            {
                "epoch": epoch,
                "lr": round(float(optimizer.param_groups[0]["lr"]), 6),
                "train_loss": round(epoch_tr_loss, 5),
                "train_policy_loss": round(epoch_tr_p_loss, 5),
                "train_value_mse": round(epoch_tr_v_loss, 5),
                "train_acc": round(epoch_tr_acc, 5),
                "val_loss": round(val_loss, 5),
                "val_policy_loss": round(val_m["policy_loss"], 5),
                "val_value_mse": round(val_m["value_mse"], 5),
                "val_value_mae": round(val_m["value_mae"], 5),
                "val_acc": round(val_acc, 5),
                "val_top2_acc": round(val_m["top2_acc"], 5),
            }
        )

    total_time = time.perf_counter() - start_train

    # Nạp lại checkpoint tốt nhất để đánh giá khách quan trên tập Test độc lập
    ckpt_data = torch.load(best_ckpt_file, map_location=device, weights_only=False)
    model.load_state_dict(ckpt_data["model_state_dict"])
    model.eval()

    test_metrics = None
    if test_loader is not None and len(test_dataset) > 0:
        tm = evaluate(model, test_loader, device, eval_policy_criterion, value_criterion)
        test_metrics = {k: (round(v, 5) if isinstance(v, float) else v) for k, v in tm.items()}
        print(
            f"\n[*] Đánh giá trên tập TEST độc lập ({tm['samples']} mẫu): "
            f"Loss={tm['loss']:.4f} | PolicyLoss={tm['policy_loss']:.4f} | ValueMSE={tm['value_mse']:.4f} | "
            f"Top-1 Acc={tm['acc'] * 100:.2f}% | Top-2 Acc={tm['top2_acc'] * 100:.2f}%"
        )

    # Đo độ trễ suy luận đơn mẫu (1, 2, 6, 7)
    dummy_x = torch.zeros((1, 2, 6, 7), dtype=torch.float32, device=device)
    with torch.inference_mode():
        for _ in range(10):
            model(dummy_x)
        latencies_ms = []
        for _ in range(200):
            t0 = time.perf_counter()
            model(dummy_x)
            latencies_ms.append((time.perf_counter() - t0) * 1000.0)
    lat_sorted = sorted(latencies_ms)
    infer_bench = {
        "mean_ms": round(float(np.mean(latencies_ms)), 4),
        "p95_ms": round(float(lat_sorted[int(0.95 * (len(lat_sorted) - 1))]), 4),
    }

    fig_file = Path(figures_dir) / "nn_learning_curves.png"
    _plot_learning_curves(history, test_metrics, fig_file)

    report_payload = {
        "seed": seed,
        "device": str(device),
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "torch_version": torch.__version__,
        "num_parameters": num_params,
        "hyperparameters": {
            "epochs": epochs,
            "batch_size": batch_size,
            "lr": lr,
            "weight_decay": weight_decay,
            "label_smoothing": label_smoothing,
            "num_res_blocks": 3,
            "num_filters": 64,
            "value_loss_weight": 0.5,
        },
        "dataset_sizes": {
            "train": len(train_dataset),
            "val": len(val_dataset),
            "test": len(test_dataset) if test_dataset else 0,
        },
        "best_epoch": best_epoch,
        "best_val_loss": round(best_val_loss, 5),
        "test_metrics": test_metrics,
        "single_inference_latency": infer_bench,
        "training_time_s": round(total_time, 2),
        "history": history,
    }
    with open(ckpt_path / "training_history.json", "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2, ensure_ascii=False)

    print(f"[+] Huấn luyện hoàn tất trong {total_time:.1f}s! Độ trễ suy luận trung bình: {infer_bench['mean_ms']:.3f} ms")
    print(f"[+] Checkpoint tốt nhất: {best_ckpt_file} (Epoch {best_epoch}, Val Loss: {best_val_loss:.4f})")
    print(f"[+] Biểu đồ đường cong học tập đã lưu tại: {fig_file}")

    return best_ckpt_file


def main():
    p = argparse.ArgumentParser(description="Huấn luyện mô hình Policy-Value ResNet cho Connect Four")
    p.add_argument("--data-dir", default="data")
    p.add_argument("--checkpoint-dir", default="checkpoints")
    p.add_argument("--figures-dir", default="results/figures")
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--lr", type=float, default=1.5e-3)
    p.add_argument("--weight-decay", type=float, default=1e-3)
    p.add_argument("--label-smoothing", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    train_policy_net(
        data_dir=args.data_dir,
        checkpoint_dir=args.checkpoint_dir,
        figures_dir=args.figures_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        weight_decay=args.weight_decay,
        label_smoothing=args.label_smoothing,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
