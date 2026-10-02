def validate(board, word):
    assert isinstance(board, list) and 1 <= len(board) <= 6, "1 <= rows <= 6"
    n = len(board[0])
    assert 1 <= n <= 6 and all(isinstance(r, list) and len(r) == n for r in board), "1 <= columns <= 6, equal rows"
    assert all(type(c) is str and len(c) == 1 and "a" <= c <= "z" for r in board for c in r), "lowercase letters"
    assert type(word) is str and 1 <= len(word) <= 15 and all("a" <= c <= "z" for c in word), "1 <= word.length <= 15"
