def validate(board):
    assert isinstance(board, list) and 1 <= len(board) <= 200, "1 <= board.length <= 200"
    n = len(board[0])
    assert 1 <= n <= 200, "1 <= board[i].length <= 200"
    assert all(isinstance(r, list) and len(r) == n for r in board), "all rows have the same length"
    assert all(v in (0, 1) and type(v) is int for r in board for v in r), "cells are 0 or 1"
