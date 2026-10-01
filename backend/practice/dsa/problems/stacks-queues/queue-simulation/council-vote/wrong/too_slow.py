class Solution:
    # Mistake: removes silenced members from a Python list, which shifts everything after them: O(n^2).
    def councilWinner(self, council):
        alive = list(council)
        i = 0
        while True:
            c = alive[i]
            j = i + 1
            while j < len(alive) and alive[j] == c:
                j += 1
            if j == len(alive):
                j = 0
                while j < i and alive[j] == c:
                    j += 1
                if j == i:
                    return "Larks" if c == "L" else "Owls"
            alive.pop(j)
            if j < i:
                i -= 1
            i = (i + 1) % len(alive)
