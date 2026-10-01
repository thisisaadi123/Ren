def validate(council):
    assert type(council) is str and 1 <= len(council) <= 100_000, "1 <= council.length <= 10^5"
    assert all(c in "LO" for c in council), "only L and O"
