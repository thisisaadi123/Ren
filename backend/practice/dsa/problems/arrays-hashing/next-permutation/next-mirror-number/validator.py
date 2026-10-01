def validate(code):
    assert type(code) is str and 1 <= len(code) <= 100_000, "1 <= code.length <= 10^5"
    assert all("0" <= c <= "9" for c in code), "code has digits only"
    assert code == code[::-1], "code reads the same from both ends"
    assert code[0] != "0", "code doesn't start with 0"
