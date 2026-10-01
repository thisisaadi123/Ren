def validate(s, words):
    assert type(s) is str and 1 <= len(s) <= 10_000, "1 <= s.length <= 10^4"
    assert isinstance(words, list) and 1 <= len(words) <= 5000, "1 <= words.length <= 5000"
    assert all(type(x) is str and 1 <= len(x) <= 30 for x in words), "1 <= words[i].length <= 30"
    assert len({len(x) for x in words}) == 1, "all words have the same length"
    assert all("a" <= c <= "z" for c in s), "s has lowercase letters only"
    assert all("a" <= c <= "z" for x in words for c in x), "words have lowercase letters only"
