from ren_check import text as check_text
def validate(text, dictionary):
    check_text("text", text, 1, 1000, "abcdefghijklmnopqrstuvwxyz")
    assert isinstance(dictionary, list) and 1 <= len(dictionary) <= 1000, "dictionary must have 1 to 1000 words"
    for w in dictionary:
        check_text("each word", w, 1, 1000, "abcdefghijklmnopqrstuvwxyz")
