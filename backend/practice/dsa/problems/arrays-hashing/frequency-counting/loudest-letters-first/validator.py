from ren_check import text
import string
def validate(s):
    text("s", s, 1, 100_000, string.ascii_letters + string.digits)
