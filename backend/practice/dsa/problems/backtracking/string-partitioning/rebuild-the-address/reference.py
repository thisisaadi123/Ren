class Solution:
    def rebuildAddress(self, digits):
        n, out, parts = len(digits), [], []

        def go(i):
            if len(parts) == 4:
                if i == n:
                    out.append(".".join(parts))
                return
            left = 4 - len(parts)
            if n - i < left or n - i > 3 * left:
                return
            for k in range(1, 4):
                p = digits[i:i + k]
                if len(p) < k or (len(p) > 1 and p[0] == "0") or int(p) > 255:
                    break
                parts.append(p)
                go(i + k)
                parts.pop()

        go(0)
        return sorted(out)
