def validate(scores, k):
    assert isinstance(scores, list) and 1 <= len(scores) <= 16, "1 <= scores.length <= 16"
    assert all(type(x) is int and 1 <= x <= 10**4 for x in scores), "1 <= scores[i] <= 10^4"
    assert type(k) is int and 1 <= k <= len(scores), "1 <= k <= scores.length"
