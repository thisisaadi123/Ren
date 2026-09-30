from ren_check import text as txt, integer
def validate(text, tag):
    txt("text", text, 1, 10**5, "abcdefghijklmnopqrstuvwxyz")
    txt("tag", tag, 1, len(text), "abcdefghijklmnopqrstuvwxyz")
