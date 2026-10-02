def validate(s):
    assert type(s) is str and 1 <= len(s) <= 30_000, "1 <= s.length <= 3 * 10^4"
    assert all(c in "0123456789-()" for c in s), "digits, '-' and parentheses only"
    i, depth = 0, 0

    def number(i):
        j = i + 1 if s[i] == "-" else i
        k = j
        while k < len(s) and s[k].isdigit():
            k += 1
        assert k > j, "a value is expected at %d" % i
        assert -1000 <= int(s[i:k]) <= 1000, "-1000 <= value <= 1000"
        return k

    def node(i, d):
        assert d < 20_000, "too deep"
        i = number(i)
        groups = 0
        while i < len(s) and s[i] == "(" and groups < 2:
            if s[i + 1] == ")":
                assert groups == 0 and i + 2 < len(s) and s[i + 2] == "(", "() only stands for an empty left child before a right child"
                i += 2
            else:
                i = node(i + 1, d + 1)
                assert i < len(s) and s[i] == ")", "unbalanced parentheses"
                i += 1
            groups += 1
        return i

    import sys
    sys.setrecursionlimit(100_000)
    end = node(0, 0)
    assert end == len(s), "extra characters after the tree"
