class Solution:
    # Mistake: breaks when a value is >= what's left, so a stamp that exactly finishes the mix is never used.
    def stampMixes(self, stamps, target):
        s = sorted(stamps)
        out, cur = [], []
        def go(start, left):
            if left == 0:
                out.append(cur[:])
                return
            for i in range(start, len(s)):
                if s[i] >= left:
                    break
                cur.append(s[i])
                go(i, left - s[i])
                cur.pop()
        go(0, target)
        return out
