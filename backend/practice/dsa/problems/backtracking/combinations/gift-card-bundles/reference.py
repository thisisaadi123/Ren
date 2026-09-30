class Solution:
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
                if i > start and c[i] == c[i - 1]:
                    continue
                cur.append(c[i])
                go(i + 1, left - c[i])
                cur.pop()

        go(0, target)
        return out
