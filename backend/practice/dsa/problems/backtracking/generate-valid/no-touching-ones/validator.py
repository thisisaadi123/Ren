def validate(n, ones):
    from math import comb
    assert type(n) is int and 1 <= n <= 20, "1 <= n <= 20"
    assert type(ones) is int and 0 <= ones <= n, "0 <= ones <= n"
    assert comb(n - ones + 1, ones) <= 10**5, "at most 10^5 strings"
