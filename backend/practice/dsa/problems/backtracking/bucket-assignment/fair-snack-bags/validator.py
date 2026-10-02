def validate(bags, kids):
    assert isinstance(bags, list) and 2 <= len(bags) <= 10, "2 <= bags.length <= 10"
    assert all(type(x) is int and 1 <= x <= 10**5 for x in bags), "1 <= bags[i] <= 10^5"
    assert type(kids) is int and 2 <= kids <= len(bags), "2 <= kids <= bags.length"
