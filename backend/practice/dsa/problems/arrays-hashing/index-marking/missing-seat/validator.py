from ren_check import ints
def validate(seats):
    ints("seats", seats, 1, 100_000, 0, len(seats))
    assert len(set(seats)) == len(seats), "seat numbers are distinct"
