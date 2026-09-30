class Solution:
    def findAll(self, text, tag):
        m = len(tag)
        fail = [0] * m
        k = 0
        for i in range(1, m):
            while k and tag[i] != tag[k]:
                k = fail[k - 1]
            if tag[i] == tag[k]:
                k += 1
            fail[i] = k
        out = []
        k = 0
        for i, c in enumerate(text):
            while k and c != tag[k]:
                k = fail[k - 1]
            if c == tag[k]:
                k += 1
            if k == m:
                out.append(i - m + 1)
                k = fail[k - 1]
        return out
