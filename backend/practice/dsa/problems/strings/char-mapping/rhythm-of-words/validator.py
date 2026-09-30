from ren_check import text
def validate(pattern, sentence):
    text("pattern", pattern, 1, 300, "abcdefghijklmnopqrstuvwxyz")
    text("sentence", sentence, 1, 3000, "abcdefghijklmnopqrstuvwxyz ")
    assert all(sentence.split(" ")), "words are separated by single spaces, with no spaces at either end"
