class Solution:
    def canColour(self, n, borders, m):
        adj = [[] for _ in range(n)]
        for a, b in borders:
            adj[a].append(b)
            adj[b].append(a)
        colour = [-1] * n

        def go(i):
            if i == n:
                return True
            taken = {colour[j] for j in adj[i]}
            for c in range(m):
                if c not in taken:
                    colour[i] = c
                    if go(i + 1):
                        return True
            colour[i] = -1
            return False

        return go(0)
