class Solution:
    # Mistake: only tries giving each kid a contiguous run of bags.
    def fairestSplit(self, bags, kids):
        n = len(bags)
        best = [sum(bags)]

        def go(i, left, worst):
            if i == n:
                if left == 0:
                    best[0] = min(best[0], worst)
                return
            if left == 0:
                return
            s = 0
            for j in range(i, n):
                s += bags[j]
                go(j + 1, left - 1, max(worst, s))

        go(0, kids, 0)
        return best[0]
