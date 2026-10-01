def validate(path):
    assert type(path) is str and 1 <= len(path) <= 30_000, "1 <= path.length <= 3 * 10^4"
    assert path[0] == "/", "path starts with /"
    assert all(c.isascii() and (c.isalnum() or c in "./_") for c in path), "letters, digits, '.', '/' and '_' only"
