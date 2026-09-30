from ren_check import ints, integer
def validate(books, hours):
    ints("books", books, 1, 10_000, 1, 10**9)
    integer("hours", hours, len(books), 10**9)
