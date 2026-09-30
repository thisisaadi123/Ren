from ren_check import text, ints
LOW = "abcdefghijklmnopqrstuvwxyz"
def validate(words, tiles, points):
    assert isinstance(words, list) and 1 <= len(words) <= 14, "1 ≤ words.length ≤ 14"
    for w in words:
        text("words[i]", w, 1, 15, LOW)
    text("tiles", tiles, 1, 100, LOW)
    ints("points", points, 26, 26, 0, 10)
