class Solution:
    def canReshape(self, a, b):
        # Swaps reach every order, so a state is the sorted word. Explore every relabel.
        start, goal = "".join(sorted(a)), "".join(sorted(b))
        seen, stack = {start}, [start]
        while stack:
            w = stack.pop()
            if w == goal:
                return True
            present = sorted(set(w))
            for x in present:
                for y in present:
                    if x < y:
                        nxt = "".join(sorted(y if c == x else x if c == y else c for c in w))
                        if nxt not in seen:
                            seen.add(nxt)
                            stack.append(nxt)
        return False
