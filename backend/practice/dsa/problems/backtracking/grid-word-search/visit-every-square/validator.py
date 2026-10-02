def validate(floor):
    assert isinstance(floor, list) and floor, "the floor has at least one row"
    n = len(floor[0])
    assert all(isinstance(r, list) and len(r) == n for r in floor), "rows have equal length"
    assert 1 <= len(floor) * n <= 20, "1 <= rows * columns <= 20"
    vals = [v for r in floor for v in r]
    assert all(v in (-1, 0, 1, 2) and type(v) is int for v in vals), "cells are -1, 0, 1 or 2"
    assert vals.count(1) == 1 and vals.count(2) == 1, "exactly one start and one end"
