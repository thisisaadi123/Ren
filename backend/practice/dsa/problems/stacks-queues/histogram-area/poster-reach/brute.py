class Solution:
    def posterReach(self, panels):
        n = len(panels)
        res = []
        for i in range(n):
            w = 0
            for a in range(n):
                for b in range(a, n):
                    if a <= i <= b and min(panels[a:b + 1]) >= panels[i]:
                        w = max(w, b - a + 1)
            res.append(w)
        return res
