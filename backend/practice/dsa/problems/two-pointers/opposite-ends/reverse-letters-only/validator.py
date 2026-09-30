from ren_check import text as check_text
def validate(text):
    check_text("text", text, 1, 100_000)
    assert all(32 <= ord(c) <= 126 for c in text), "text must be printable ASCII"
