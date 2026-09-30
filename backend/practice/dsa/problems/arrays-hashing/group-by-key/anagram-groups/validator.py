import string
def validate(words):
    assert isinstance(words, list) and 1 <= len(words) <= 10_000, "1 to 10^4 words"
    for w in words:
        assert isinstance(w, str) and len(w) <= 30 and set(w) <= set(string.ascii_lowercase), "words are up to 30 lowercase letters"
