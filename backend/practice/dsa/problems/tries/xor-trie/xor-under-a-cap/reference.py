class Solution:
    def xorUnderCap(self, nums, queries):
        nums = sorted(nums)
        order = sorted(range(len(queries)), key=lambda i: queries[i][1])
        root = [None, None]
        out = [-1] * len(queries)
        k = 0
        for qi in order:
            x, m = queries[qi]
            while k < len(nums) and nums[k] <= m:
                node, v = root, nums[k]
                for b in range(29, -1, -1):
                    bit = v >> b & 1
                    if node[bit] is None:
                        node[bit] = [None, None]
                    node = node[bit]
                k += 1
            if k == 0:
                continue
            node, best = root, 0
            for b in range(29, -1, -1):
                bit = x >> b & 1
                if node[bit ^ 1] is not None:
                    best |= 1 << b
                    node = node[bit ^ 1]
                else:
                    node = node[bit]
            out[qi] = best
        return out
