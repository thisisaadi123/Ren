from ren_check import text as check_text
def validate(word, text):
    check_text("word", word, 0, 100, "abcdefghijklmnopqrstuvwxyz")
    check_text("text", text, 0, 100_000, "abcdefghijklmnopqrstuvwxyz")
