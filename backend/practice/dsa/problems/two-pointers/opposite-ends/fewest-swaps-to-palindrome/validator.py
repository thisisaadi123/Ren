import collections
from ren_check import text
def validate(word):
    text("word", word, 1, 2000, "abcdefghijklmnopqrstuvwxyz")
    odd = sum(1 for c in collections.Counter(word).values() if c % 2)
    assert odd <= 1, "word must be rearrangeable into a palindrome"
