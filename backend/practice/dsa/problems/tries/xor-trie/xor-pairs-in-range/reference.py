class Solution:
    def xorPairsInRange(self, nums, low, high):
        B = 15

        def count_below(limit):
            root = [None, None, 0]
            total = 0
            for x in nums:
                node = root
                for b in range(B - 1, -1, -1):
                    if node is None:
                        break
                    xb, lb = x >> b & 1, limit >> b & 1
                    if lb:
                        same = node[xb]
                        if same is not None:
                            total += same[2]
                        node = node[xb ^ 1]
                    else:
                        node = node[xb]
                node = root
                for b in range(B - 1, -1, -1):
                    bit = x >> b & 1
                    if node[bit] is None:
                        node[bit] = [None, None, 0]
                    node = node[bit]
                    node[2] += 1
            return total

        return count_below(high + 1) - count_below(low)
