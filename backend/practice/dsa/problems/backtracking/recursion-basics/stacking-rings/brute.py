class Solution:
    def ringMoves(self, n):
        # Iterative rule: alternate moving the smallest ring cyclically with the only other legal move.
        pegs = {1: list(range(n, 0, -1)), 2: [], 3: []}
        cycle = [1, 3, 2] if n % 2 else [1, 2, 3]
        out, at = [], 0
        while len(pegs[3]) < n:
            a, b = cycle[at], cycle[(at + 1) % 3]
            pegs[b].append(pegs[a].pop())
            out.append([a, b])
            at = (at + 1) % 3
            if len(pegs[3]) == n:
                break
            x, y = [p for p in (1, 2, 3) if p != b]
            if pegs[x] and (not pegs[y] or pegs[x][-1] < pegs[y][-1]):
                pegs[y].append(pegs[x].pop())
                out.append([x, y])
            else:
                pegs[x].append(pegs[y].pop())
                out.append([y, x])
        return out
