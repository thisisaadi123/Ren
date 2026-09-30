import string
from ren_check import text as txt
def validate(text):
    txt("text", text, 0, 200, string.ascii_letters + string.digits + " +-_.")
