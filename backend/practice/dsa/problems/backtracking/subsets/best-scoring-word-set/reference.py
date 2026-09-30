class Solution:
    def bestWordSet(self, words, tiles, points):
        bag = [0] * 26
        for ch in tiles:
            bag[ord(ch) - 97] += 1
        need, value = [], []
        for w in words:
            c = [0] * 26
            for ch in w:
                c[ord(ch) - 97] += 1
            if all(c[j] <= bag[j] for j in range(26)):
                need.append([(j, c[j]) for j in range(26) if c[j]])
                value.append(sum(points[ord(ch) - 97] for ch in w))
        n = len(need)
        suffix = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix[i] = suffix[i + 1] + value[i]
        best = 0

        def go(i, score):
            nonlocal best
            if score > best:
                best = score
            if i == n or score + suffix[i] <= best:
                return
            if all(bag[j] >= c for j, c in need[i]):
                for j, c in need[i]:
                    bag[j] -= c
                go(i + 1, score + value[i])
                for j, c in need[i]:
                    bag[j] += c
            go(i + 1, score)

        go(0, 0)
        return best
