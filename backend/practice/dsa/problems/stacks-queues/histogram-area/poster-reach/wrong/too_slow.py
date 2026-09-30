class Solution:
    # Mistake: walks outward from every panel: O(n²) when panels are equal.
    def posterReach(self, panels):
        n = len(panels)
        res = []
        for i in range(n):
            a = i
            while a > 0 and panels[a - 1] >= panels[i]:
                a -= 1
            b = i
            while b + 1 < n and panels[b + 1] >= panels[i]:
                b += 1
            res.append(b - a + 1)
        return res
