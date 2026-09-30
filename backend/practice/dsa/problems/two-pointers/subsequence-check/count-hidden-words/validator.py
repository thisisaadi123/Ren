from ren_check import text as check_text
def validate(text, words):
    check_text("text", text, 1, 50_000, "abcdefghijklmnopqrstuvwxyz")
    assert isinstance(words, list) and 1 <= len(words) <= 5000, "words must have 1 to 5000 words"
    for w in words:
        check_text("each word", w, 1, 50, "abcdefghijklmnopqrstuvwxyz")
