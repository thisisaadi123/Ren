def validate(products, typed):
    assert isinstance(products, list) and 1 <= len(products) <= 1000, "1 <= products.length <= 1000"
    for s in products + [typed]:
        assert type(s) is str and 1 <= len(s) <= 100 and all("a" <= c <= "z" for c in s), "1 <= length <= 100, lowercase"
