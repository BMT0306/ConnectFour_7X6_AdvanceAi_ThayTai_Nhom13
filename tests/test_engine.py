"""Kiểm thử engine: chạy MỌI test trên cả bitboard (Connect4) và bản tham chiếu."""
import random

import numpy as np
import pytest

from c4.game import COLS, PLAYER1, PLAYER2, IllegalMoveError
from helpers import ENGINES, play, random_game_moves

# ---- các ván dựng sẵn (cột 0..6). Đã kiểm chứng: thắng ĐÚNG ở nước cuối, không sớm hơn ----
P1_HORIZONTAL = [0, 0, 1, 1, 2, 2, 3]            # X: hàng 0, cột 0-3
P1_VERTICAL = [0, 1, 0, 1, 0, 1, 0]              # X: cột 0 x4
P2_VERTICAL = [0, 1, 2, 1, 2, 1, 3, 1]           # O: cột 1 x4
P2_HORIZONTAL = [0, 3, 0, 4, 1, 5, 1, 6]         # O: hàng 0, cột 3-6
P1_DIAG_SLASH = [0, 1, 1, 2, 6, 2, 2, 3, 6, 3, 6, 3, 3]   # X: đường chéo '/'  (0,0)-(3,3)
P1_DIAG_BACK = [6 - c for c in P1_DIAG_SLASH]              # X: đường chéo '\' (đối xứng gương)

WIN_CASES = [
    ("P1 ngang", P1_HORIZONTAL, PLAYER1),
    ("P1 dọc", P1_VERTICAL, PLAYER1),
    ("P2 dọc", P2_VERTICAL, PLAYER2),
    ("P2 ngang", P2_HORIZONTAL, PLAYER2),
    ("P1 chéo /", P1_DIAG_SLASH, PLAYER1),
    ("P1 chéo \\", P1_DIAG_BACK, PLAYER1),
]

# Ván hòa trọn 42 nước (tìm bằng tìm kiếm ngẫu nhiên có seed, đã kiểm chứng bằng cả 2 engine)
DRAW_GAME = [3, 1, 1, 4, 5, 6, 4, 1, 3, 4, 5, 3, 2, 0, 0, 5, 4, 5, 1, 5, 5, 4, 1, 6, 1, 2, 3, 4,
             3, 0, 0, 3, 2, 0, 6, 6, 0, 2, 2, 6, 2, 6]
# Ván mà nước thứ 42 (cuối cùng) cho PLAYER2 thắng -> phải tính là THẮNG, không phải hòa
LAST_MOVE_WIN_GAME = [5, 2, 5, 1, 4, 5, 4, 0, 1, 4, 2, 0, 3, 2, 0, 6, 5, 2, 0, 4, 6, 2, 5, 4, 6, 3,
                      3, 3, 0, 1, 3, 6, 5, 0, 2, 3, 1, 6, 6, 1, 1, 4]


def test_initial_state():
    for E in ENGINES:
        g = E()
        assert g.legal_actions() == list(range(COLS))
        assert g.current_player == PLAYER1
        assert g.move_count == 0
        assert g.winner == 0 and not g.is_terminal()
        assert not g.to_array().any()


def test_gravity_and_turns():
    for E in ENGINES:
        g = E()
        g.step(3)
        g.step(3)
        g.step(3)
        arr = g.to_array()
        assert [int(arr[r, 3]) for r in range(3)] == [1, -1, 1]  # hàng 0 ở dưới cùng
        assert g.current_player == PLAYER2
        assert g.move_count == 3


def test_all_win_types_detected_only_on_last_move():
    for E in ENGINES:
        for name, seq, who in WIN_CASES:
            g = E()
            for i, c in enumerate(seq):
                assert not g.is_terminal(), f"{E.__name__} {name}: kết thúc sớm ở nước {i}"
                g.step(c)
            assert g.is_terminal(), f"{E.__name__} {name}: chưa nhận ra thắng"
            assert g.winner == who, f"{E.__name__} {name}"
            assert g.result(who) == 1 and g.result(-who) == -1
            assert g.legal_actions() == []


def test_full_board_draw():
    for E in ENGINES:
        g = play(E(), DRAW_GAME)
        assert g.move_count == 42
        assert g.is_terminal() and g.winner == 0
        assert g.result(PLAYER1) == 0 and g.result(PLAYER2) == 0
        assert g.legal_actions() == []


def test_win_on_last_move_counts_as_win_not_draw():
    for E in ENGINES:
        g = play(E(), LAST_MOVE_WIN_GAME[:-1])
        assert not g.is_terminal()
        g.step(LAST_MOVE_WIN_GAME[-1])
        assert g.move_count == 42
        assert g.winner == PLAYER2
        assert g.result(PLAYER2) == 1


def test_result_before_terminal_raises():
    for E in ENGINES:
        with pytest.raises(ValueError):
            E().result()


def test_illegal_moves():
    for E in ENGINES:
        g = E()
        for bad in (-1, 7, 100):
            with pytest.raises(IllegalMoveError):
                g.step(bad)
        with pytest.raises(IllegalMoveError):
            g.step("a")
        with pytest.raises(IllegalMoveError):
            g.step(1.5)
        # cột 0 đầy sau 6 quân (xen kẽ màu nên chưa ai thắng)
        for _ in range(6):
            g.step(0)
        assert 0 not in g.legal_actions()
        with pytest.raises(IllegalMoveError):
            g.step(0)
        # đi tiếp sau khi game kết thúc
        g2 = play(E(), P1_HORIZONTAL)
        with pytest.raises(IllegalMoveError):
            g2.step(4)
        # hoàn tác khi chưa có nước nào
        with pytest.raises(IllegalMoveError):
            E().undo()


def test_numpy_int_actions_accepted():
    for E in ENGINES:
        g = E()
        g.step(np.int64(3))
        assert g.to_array()[0, 3] == 1


def test_undo_restores_every_state():
    rng = random.Random(7)
    for E in ENGINES:
        for _ in range(60):
            g = E()
            snaps = [(g.key(), g.to_array().copy(), g.winner, g.current_player, g.legal_actions())]
            seq = random_game_moves(random.Random(rng.random()), E)
            for c in seq:
                g.step(c)
                snaps.append((g.key(), g.to_array().copy(), g.winner, g.current_player, g.legal_actions()))
            for i in range(len(seq), 0, -1):
                assert g.undo() == seq[i - 1]
                key, arr, win, cur, legal = snaps[i - 1]
                assert g.key() == key
                assert np.array_equal(g.to_array(), arr)
                assert (g.winner, g.current_player, g.legal_actions()) == (win, cur, legal)


def test_clone_is_independent():
    for E in ENGINES:
        g = play(E(), [3, 3, 4])
        h = g.clone()
        h.step(2)
        h.step(0)
        assert g.move_count == 3 and h.move_count == 5
        assert not np.array_equal(g.to_array(), h.to_array())
        g.undo()
        assert h.move_count == 5  # sửa bản gốc không ảnh hưởng bản sao


def test_relative_array_and_encode():
    for E in ENGINES:
        g = play(E(), [3])  # X vừa đi, tới lượt O
        assert g.to_array()[0, 3] == 1
        assert g.to_array(relative=True)[0, 3] == -1  # góc nhìn của O: quân X là đối thủ
        enc = g.encode()
        assert enc.shape == (2, 6, 7) and enc.dtype == np.float32
        assert enc[0].sum() == 0 and enc[1][0, 3] == 1  # kênh 0 = quân của mình (O) chưa có gì


def test_key_identifies_positions_regardless_of_move_order():
    for E in ENGINES:
        a = play(E(), [0, 1, 2, 3])
        b = play(E(), [2, 1, 0, 3])
        c = play(E(), [0, 1, 3, 2])  # cùng số quân nhưng màu khác -> vị trí khác
        assert a.key() == b.key()
        assert a.key() != c.key()


def test_winning_moves_for_both_sides():
    for E in ENGINES:
        # X có 3 quân hàng đáy cột 3,4,5; tới lượt O -> O cần chặn cột 2 và 6
        g = play(E(), [3, 0, 4, 0, 5])
        assert g.current_player == PLAYER2
        assert g.winning_moves() == []  # O chưa có nước thắng ngay
        assert g.winning_moves(PLAYER1) == [2, 6]  # X đang đe dọa cột 2 và 6
        # không làm thay đổi trạng thái
        assert g.move_count == 5
        # ván kết thúc thì không còn nước thắng
        assert play(E(), P1_HORIZONTAL).winning_moves() == []


def test_perft_depth_has_no_wins_before_ply_7():
    # Chưa thể có ai thắng trước nước thứ 7 => số chuỗi nước đi độ sâu 6 đúng bằng 7^6.
    def perft(g, depth):
        if depth == 0:
            return 1
        total = 0
        for c in g.legal_actions():
            g.step(c)
            total += perft(g, depth - 1)
            g.undo()
        return total

    assert perft(ENGINES[0](), 6) == 7 ** 6 == 117649
    assert perft(ENGINES[1](), 4) == 7 ** 4 == 2401
