"""Kiểm thử quy trình sinh dữ liệu sạch (không nhiễu nhãn, không rò rỉ chéo) và tăng cường đối xứng."""
from __future__ import annotations

import random
import numpy as np

from c4.agents import AlphaBetaAgent, Budget
from c4.game import Connect4
from c4.train.gen_data import augment_horizontal_flip, generate_dataset, generate_game


def test_generate_game_keeps_clean_expert_labels_under_high_epsilon():
    """Ngay cả khi epsilon=1.0 (luôn đi bước khám phá ngẫu nhiên), nhãn action lưu lại vẫn phải là nước của chuyên gia."""
    rng = random.Random(123)
    teacher = AlphaBetaAgent(seed=0, depth=2)
    samples = generate_game(
        game_id=0,
        depth=2,
        opening_plies=2,
        epsilon=1.0,
        pure_after_ply=12,
        rng=rng,
        agent=teacher,
    )
    assert len(samples) > 0
    for s in samples:
        assert s["state"].shape == (2, 6, 7)
        assert s["legal_mask"][s["action"]] == True  # noqa: E712
        assert s["value"] in (-1.0, 0.0, 1.0)


def test_horizontal_flip_symmetry():
    g = Connect4()
    g.step(1)  # cột 1 -> khi lật ngang thành cột 5 (6 - 1)
    st = g.encode()[None, ...]
    act = np.array([2], dtype=np.int64)
    mask = np.array([[True, True, True, True, True, True, False]], dtype=bool)
    val = np.array([1.0], dtype=np.float32)

    aug_s, aug_a, aug_m, aug_v = augment_horizontal_flip(st, act, mask, val)
    assert aug_s.shape == (2, 2, 6, 7)
    assert aug_a[1] == 4  # 6 - 2
    assert aug_m[1, 0] == False and aug_m[1, 6] == True  # noqa: E712
    assert aug_v[1] == 1.0


def test_dataset_split_zero_cross_leakage(tmp_path):
    stats = generate_dataset(
        num_games=20,
        depth=2,
        opening_plies=2,
        epsilon=0.2,
        seed=99,
        out_dir=tmp_path,
        augment_train=True,
        deduplicate=True,
    )
    assert stats["train_samples"] > 0
    tr = np.load(tmp_path / "train.npz")["states"]
    va = np.load(tmp_path / "val.npz")["states"]
    te = np.load(tmp_path / "test.npz")["states"]

    tr_keys = {np.ascontiguousarray(s).tobytes() for s in tr}
    va_keys = {np.ascontiguousarray(s).tobytes() for s in va}
    te_keys = {np.ascontiguousarray(s).tobytes() for s in te}

    assert len(tr_keys & va_keys) == 0, "Rò rỉ trạng thái giữa Train và Val!"
    assert len(tr_keys & te_keys) == 0, "Rò rỉ trạng thái giữa Train và Test!"
    assert len(va_keys & te_keys) == 0, "Rò rỉ trạng thái giữa Val và Test!"

