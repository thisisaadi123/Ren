import collections
class Solution:
    def minSwapsToPalindrome(self, word):
        start = word
        seen = {start: 0}
        q = collections.deque([start])
        while q:
            w = q.popleft()
            if w == w[::-1]:
                return seen[w]
            for i in range(len(w) - 1):
                if w[i] != w[i + 1]:
                    v = w[:i] + w[i + 1] + w[i] + w[i + 2:]
                    if v not in seen:
                        seen[v] = seen[w] + 1
                        q.append(v)
