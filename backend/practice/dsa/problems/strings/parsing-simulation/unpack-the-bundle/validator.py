def validate(bundle):
    assert isinstance(bundle, str) and len(bundle) <= 10**5, "bundle has at most 10^5 characters"
    assert all(32 <= ord(c) <= 126 for c in bundle), "bundle has printable ASCII characters only"
    i, n = 0, len(bundle)
    while i < n:
        j = i
        while j < n and "0" <= bundle[j] <= "9":
            j += 1
        assert i < j < n and bundle[j] == "#", "each string starts with its length and a #"
        assert bundle[i] != "0" or j == i + 1, "lengths have no leading zeros"
        i = j + 1 + int(bundle[i:j])
        assert i <= n, "a string runs past the end of the bundle"
