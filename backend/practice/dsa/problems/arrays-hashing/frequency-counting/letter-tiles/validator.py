from ren_check import text
import string
def validate(sign, tiles):
    text("sign", sign, 1, 100_000, string.ascii_lowercase)
    text("tiles", tiles, 1, 100_000, string.ascii_lowercase)
