def validate(board, words):
    assert isinstance(board, list) and 1 <= len(board) <= 8, "1 <= rows <= 8"
    n = len(board[0])
    assert 1 <= n <= 8 and all(type(r) is str and len(r) == n and all("a" <= c <= "z" for c in r) for r in board), "rows of equal length 1..8, lowercase"
    assert isinstance(words, list) and 1 <= len(words) <= 5000, "1 <= words.length <= 5000"
    assert all(type(w) is str and 1 <= len(w) <= 10 and all("a" <= c <= "z" for c in w) for w in words), "words: 1..10 lowercase"
