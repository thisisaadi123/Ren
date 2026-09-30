class Solution:
    # Mistake: correct, but simulates every insertion: O(n^2) when keys arrive in sorted order.
    def arrivalDepths(self, keys):
        left, right = {}, {}
        out = [1]
        root = keys[0]
        for k in keys[1:]:
            cur, d = root, 1
            while True:
                d += 1
                nxt = left.get(cur) if k < cur else right.get(cur)
                if nxt is None:
                    (left if k < cur else right)[cur] = k
                    break
                cur = nxt
            out.append(d)
        return out
