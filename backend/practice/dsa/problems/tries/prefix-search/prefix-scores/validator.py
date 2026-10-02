def validate(words):
    assert isinstance(words, list) and 1 <= len(words) <= 2000, "1 <= words.length <= 2000"
    assert all(type(w) is str and 1 <= len(w) <= 100 and all("a" <= c <= "z" for c in w) for w in words), "1 <= length <= 100, lowercase"
