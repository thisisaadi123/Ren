def validate(mine):
    assert isinstance(mine, list) and 1 <= len(mine) <= 6, "1 <= rows <= 6"
    n = len(mine[0])
    assert 1 <= n <= 6 and all(isinstance(r, list) and len(r) == n for r in mine), "1 <= columns <= 6"
    assert all(type(v) is int and 0 <= v <= 100 for r in mine for v in r), "0 <= gold <= 100"
    assert sum(1 for r in mine for v in r if v) <= 20, "at most 20 cells hold gold"
