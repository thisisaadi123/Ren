from ren_check import text as check_text
def validate(text):
    check_text("text", text, 1, 100_000, "abcdefghijklmnopqrstuvwxyz")
