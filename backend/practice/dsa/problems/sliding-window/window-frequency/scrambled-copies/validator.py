def validate(text, word):
    assert type(text) is str and 1 <= len(text) <= 100_000, "1 <= text.length <= 10^5"
    assert type(word) is str and 1 <= len(word) <= 100_000, "1 <= word.length <= 10^5"
    assert all("a" <= c <= "z" for c in text + word), "lowercase letters only"
