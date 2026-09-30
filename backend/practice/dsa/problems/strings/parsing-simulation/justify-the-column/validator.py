import string
from ren_check import integer
def validate(words, width):
    integer("width", width, 1, 100)
    assert isinstance(words, list) and 1 <= len(words) <= 300, "words must have 1 to 300 items"
    ok = set(string.ascii_letters + string.digits + ".,!?'-")
    for w in words:
        assert isinstance(w, str) and 1 <= len(w) <= width, "every word has 1 to width characters"
        assert set(w) <= ok, "words have letters, digits and . , ! ? ' - only"
