class Solution:
    def lineUps(self, floats):
        n = len(floats)
        used = [False] * n
        out, cur = [], []

        def go():
            if len(cur) == n:
                out.append(cur[:])
                return
            for i in range(n):
                if not used[i]:
                    used[i] = True
                    cur.append(floats[i])
                    go()
                    cur.pop()
                    used[i] = False

        go()
        return out
