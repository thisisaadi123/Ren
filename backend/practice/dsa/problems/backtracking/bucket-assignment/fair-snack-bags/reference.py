class Solution:
    def fairestSplit(self, bags, kids):
        xs = sorted(bags, reverse=True)
        load = [0] * kids
        best = [sum(xs)]

        def go(i):
            if i == len(xs):
                best[0] = min(best[0], max(load))
                return
            seen = set()
            for t in range(kids):
                if load[t] in seen or load[t] + xs[i] >= best[0]:
                    continue
                seen.add(load[t])
                load[t] += xs[i]
                go(i + 1)
                load[t] -= xs[i]

        go(0)
        return best[0] if len(xs) > 0 else 0
