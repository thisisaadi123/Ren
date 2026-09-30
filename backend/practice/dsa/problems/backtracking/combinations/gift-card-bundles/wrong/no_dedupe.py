class Solution:
    # Mistake: never skips equal values, so the same bundle is listed once per choice of physical cards.
    def giftBundles(self, cards, target):
        c = sorted(cards)
        out, cur = [], []
        def go(start, left):
            if left == 0:
                out.append(cur[:])
                return
            for i in range(start, len(c)):
                if c[i] > left:
                    break
                cur.append(c[i])
                go(i + 1, left - c[i])
                cur.pop()
        go(0, target)
        return out
