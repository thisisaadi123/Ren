class Solution:
    # Mistake: explores every choice of physical cards and removes repeats with a set at the end.
    # With forty 1-cards and target 20 that is C(40, 20) paths.
    def giftBundles(self, cards, target):
        c = sorted(cards)
        seen, cur = set(), []
        def go(start, left):
            if left == 0:
                seen.add(tuple(cur))
                return
            for i in range(start, len(c)):
                if c[i] > left:
                    break
                cur.append(c[i])
                go(i + 1, left - c[i])
                cur.pop()
        go(0, target)
        return [list(t) for t in seen]
