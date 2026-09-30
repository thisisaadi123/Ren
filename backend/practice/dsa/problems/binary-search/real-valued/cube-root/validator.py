def validate(volume):
    assert type(volume) in (int, float), "volume must be a number"
    assert -10**9 <= volume <= 10**9, "-10^9 <= volume <= 10^9"
