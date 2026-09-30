def validate(pages, days):
    assert isinstance(pages, list), "pages must be a list"
    assert 1 <= len(pages) <= 50_000, "1 <= pages.length <= 5 * 10^4"
    assert all(type(p) is int and 1 <= p <= 500 for p in pages), "1 <= pages[i] <= 500"
    assert type(days) is int, "days must be an int"
    assert 1 <= days <= len(pages), "1 <= days <= pages.length"
