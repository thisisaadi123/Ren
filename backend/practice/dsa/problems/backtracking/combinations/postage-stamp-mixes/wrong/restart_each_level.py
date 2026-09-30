class Solution:
    # Mistake: every level tries all values from the smallest again, so [2, 3] and [3, 2] are both found
    # (and after sorting they appear twice).
    def stampMixes(self, stamps, target):
        s = sorted(stamps)
        out, cur = [], []
        def go(left):
            if left == 0:
                out.append(sorted(cur))
                return
            for v in s:
                if v > left:
                    break
                cur.append(v)
                go(left - v)
                cur.pop()
        go(target)
        return out
