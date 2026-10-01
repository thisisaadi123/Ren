def validate(ratings):
    assert isinstance(ratings, list) and 1 <= len(ratings) <= 100_000, "1 <= ratings.length <= 10^5"
    assert all(type(v) is int and 0 <= v <= 100 for v in ratings), "0 <= ratings[i] <= 100"
