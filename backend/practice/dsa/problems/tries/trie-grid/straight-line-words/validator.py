def validate(board, words):
    assert isinstance(board, list) and 1 <= len(board) <= 50, "1 <= rows <= 50"
    n = len(board[0])
    assert 1 <= n <= 50 and all(type(r) is str and len(r) == n and all("a" <= c <= "z" for c in r) for r in board), "rows of equal length 1..50, lowercase"
    assert isinstance(words, list) and 1 <= len(words) <= 2000, "1 <= words.length <= 2000"
    assert all(type(w) is str and 1 <= len(w) <= 50 and all("a" <= c <= "z" for c in w) for w in words), "words: 1..50 lowercase"
