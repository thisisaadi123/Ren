from ren_check import text
import string
def validate(words):
    assert isinstance(words, list) and 1 <= len(words) <= 10_000, "1 to 10^4 words"
    for w in words:
        text("word", w, 1, 50, string.ascii_lowercase)
