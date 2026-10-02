def validate(base, exp, mod):
    assert type(base) is int and 0 <= base <= 10**18, "0 <= base <= 10^18"
    assert type(exp) is int and 0 <= exp <= 10**18, "0 <= exp <= 10^18"
    assert type(mod) is int and 1 <= mod <= 10**9, "1 <= mod <= 10^9"
