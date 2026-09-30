class Solution:
    # Mistake: gives each district the first free colour and never revisits a choice.
    def canColour(self, n, borders, m):
        adj = [[] for _ in range(n)]
        for a, b in borders:
            adj[a].append(b)
            adj[b].append(a)
        colour = [-1] * n
        for i in range(n):
            taken = {colour[j] for j in adj[i]}
            free = [c for c in range(m) if c not in taken]
            if not free:
                return False
            colour[i] = free[0]
        return True
