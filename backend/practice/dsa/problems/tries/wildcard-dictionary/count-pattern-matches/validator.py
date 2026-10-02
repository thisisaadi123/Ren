def validate(words, patterns):
    assert isinstance(words, list) and 1 <= len(words) <= 5000, "1 <= words.length <= 5000"
    assert isinstance(patterns, list) and 1 <= len(patterns) <= 5000, "1 <= patterns.length <= 5000"
    assert all(type(w) is str and 1 <= len(w) <= 10 and all("a" <= c <= "z" for c in w) for w in words), "words: 1..10 lowercase"
    assert all(type(p) is str and 1 <= len(p) <= 10 and all("a" <= c <= "z" or c == "." for c in p) and p.count(".") <= 2 for p in patterns), "patterns: 1..10, at most 2 dots"
