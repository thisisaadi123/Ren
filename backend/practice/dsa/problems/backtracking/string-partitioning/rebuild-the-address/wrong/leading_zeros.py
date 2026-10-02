class Solution:
    # Mistake: allows parts with leading zeros, like 01.
    def rebuildAddress(self, digits):
        n, out = len(digits), []
        for a in range(1, 4):
            for b in range(a + 1, a + 4):
                for c in range(b + 1, b + 4):
                    if c < n and n - c <= 3:
                        parts = [digits[:a], digits[a:b], digits[b:c], digits[c:]]
                        if all(p and int(p) <= 255 for p in parts):
                            out.append(".".join(parts))
        return sorted(out)
