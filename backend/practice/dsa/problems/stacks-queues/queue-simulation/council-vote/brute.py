class Solution:
    def councilWinner(self, council):
        alive = list(council)
        banned = [False] * len(alive)
        while True:
            for i, c in enumerate(alive):
                if banned[i]:
                    continue
                rest = {alive[j] for j in range(len(alive)) if not banned[j]}
                if rest == {c}:
                    return "Larks" if c == "L" else "Owls"
                # Silence the next opponent who would speak after i, wrapping around.
                for d in range(1, len(alive) + 1):
                    j = (i + d) % len(alive)
                    if not banned[j] and alive[j] != c:
                        banned[j] = True
                        break
