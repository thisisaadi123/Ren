class Solution:
    # Mistake: recurses from i + 1, so each value can be used only once.
    def stampMixes(self, stamps, target):
        s = sorted(stamps)
        out, cur = [], []
        def go(start, left):
            if left == 0:
                out.append(cur[:])
                return
            for i in range(start, len(s)):
                if s[i] > left:
                    break
                cur.append(s[i])
                go(i + 1, left - s[i])
                cur.pop()
        go(0, target)
        return out
