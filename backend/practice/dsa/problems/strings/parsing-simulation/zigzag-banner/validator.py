import string
from ren_check import text as txt, integer
def validate(text, rows):
    txt("text", text, 1, 10**5, string.ascii_letters + string.digits + ".,")
    integer("rows", rows, 1, 1000)
