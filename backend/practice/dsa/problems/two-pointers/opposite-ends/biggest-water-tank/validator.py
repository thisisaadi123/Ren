from ren_check import ints
def validate(posts):
    ints("posts", posts, 2, 100_000, 0, 10**9)
