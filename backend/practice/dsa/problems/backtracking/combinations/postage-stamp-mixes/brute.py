class Solution:
    def stampMixes(self, stamps, target):
        # Decide how many of each value to use, one value at a time.
        s = sorted(stamps)
        out = []
        def go(i, left, cur):
            if i == len(s):
                if left == 0:
                    out.append(cur)
                return
            for c in range(left // s[i] + 1):
                go(i + 1, left - c * s[i], cur + [s[i]] * c)
        go(0, target, [])
        return out
