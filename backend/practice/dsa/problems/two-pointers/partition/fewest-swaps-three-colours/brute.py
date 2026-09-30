import collections
class Solution:
    def minSwapsThreeColours(self, balls):
        start, goal = tuple(balls), tuple(sorted(balls))
        dist = {start: 0}
        q = collections.deque([start])
        while q:
            s = q.popleft()
            if s == goal:
                return dist[s]
            for i in range(len(s)):
                for j in range(i + 1, len(s)):
                    if s[i] != s[j]:
                        t = list(s)
                        t[i], t[j] = t[j], t[i]
                        t = tuple(t)
                        if t not in dist:
                            dist[t] = dist[s] + 1
                            q.append(t)
