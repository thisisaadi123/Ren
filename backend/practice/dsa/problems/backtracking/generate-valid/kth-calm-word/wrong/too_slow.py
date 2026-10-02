class Solution:
    # Mistake: lists every calm word in order until reaching the k-th.
    def kthCalmWord(self, n, k):
        count = [0]
        res = [""]

        def go(w):
            if res[0]:
                return
            if len(w) == n:
                count[0] += 1
                if count[0] == k:
                    res[0] = w
                return
            for c in "abc":
                if not w or w[-1] != c:
                    go(w + c)

        go("")
        return res[0]
