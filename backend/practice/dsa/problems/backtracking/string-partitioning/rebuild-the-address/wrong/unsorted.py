class Solution:
    # Mistake: returns the addresses in the order found, longest first part first.
    def rebuildAddress(self, digits):
        n, out = len(digits), []
        ok = lambda p: p and (p == "0" or p[0] != "0") and int(p) <= 255
        for a in range(3, 0, -1):
            for b in range(a + 3, a, -1):
                for c in range(b + 3, b, -1):
                    if c < n and n - c <= 3:
                        parts = [digits[:a], digits[a:b], digits[b:c], digits[c:]]
                        if all(ok(p) for p in parts):
                            out.append(".".join(parts))
        return out
