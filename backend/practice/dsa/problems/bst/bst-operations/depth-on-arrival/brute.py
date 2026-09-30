class Solution:
    def arrivalDepths(self, keys):
        left, right = {}, {}
        out = [1]
        root = keys[0]
        for k in keys[1:]:
            cur, d = root, 1
            while True:
                d += 1
                side = left if k < cur else right
                if cur in side:
                    cur = side[cur]
                else:
                    side[cur] = k
                    break
            out.append(d)
        return out
