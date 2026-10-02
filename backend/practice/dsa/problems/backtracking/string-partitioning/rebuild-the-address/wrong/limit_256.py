class Solution:
    # Mistake: allows 256 as a part.
    def rebuildAddress(self, digits):
        n, out = len(digits), []
        ok = lambda p: p and (p == "0" or p[0] != "0") and int(p) <= 256
        for a in range(1, 4):
            for b in range(a + 1, a + 4):
                for c in range(b + 1, b + 4):
                    if c < n and n - c <= 3:
                        parts = [digits[:a], digits[a:b], digits[b:c], digits[c:]]
                        if all(ok(p) for p in parts):
                            out.append(".".join(parts))
        return sorted(out)
