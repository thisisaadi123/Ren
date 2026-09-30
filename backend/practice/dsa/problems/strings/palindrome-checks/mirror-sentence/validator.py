def validate(text):
    assert isinstance(text, str) and 1 <= len(text) <= 2 * 10**5, "text has 1 to 2 * 10^5 characters"
    assert all(32 <= ord(c) <= 126 for c in text), "text has printable ASCII characters only"
