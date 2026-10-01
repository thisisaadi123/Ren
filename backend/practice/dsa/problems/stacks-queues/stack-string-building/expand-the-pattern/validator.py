def validate(pattern):
    assert type(pattern) is str and 1 <= len(pattern) <= 3000, "1 <= pattern.length <= 3000"
    stack, i, size = [[0]], 0, 0
    lengths = [0]
    while i < len(pattern):
        c = pattern[i]
        if c.isdigit():
            j = i
            while j < len(pattern) and pattern[j].isdigit():
                j += 1
            k = int(pattern[i:j])
            assert pattern[i] != "0" and 1 <= k <= 300, "1 <= k <= 300, no leading zeros"
            assert j < len(pattern) and pattern[j] == "[", "every number is followed by ["
            stack.append(k)
            lengths.append(0)
            i = j + 1
            continue
        if c == "]":
            assert len(stack) > 1, "unbalanced ]"
            k = stack.pop()
            inner = lengths.pop()
            lengths[-1] += inner * k
        else:
            assert "a" <= c <= "z", "letters, digits and brackets only"
            lengths[-1] += 1
        assert lengths[-1] <= 100_000, "expanded length <= 10^5"
        i += 1
    assert len(stack) == 1, "unbalanced ["
    assert lengths[0] <= 100_000, "expanded length <= 10^5"
