class Solution:
    # Mistake: records each border only under its first district, so some conflicts are never checked.
    def canColour(self, n, borders, m):
        adj = [[] for _ in range(n)]
        for a, b in borders:
            adj[a].append(b)
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
