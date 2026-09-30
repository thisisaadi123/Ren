class Solution:
    def canRepaint(self, s, t, m):
        colours = [chr(97 + i) for i in range(m)]
        seen, stack = {s}, [s]
        while stack:
            w = stack.pop()
            if w == t:
                return True
            for x in set(w):
                for y in colours:
                    if y != x:
                        nxt = w.replace(x, y)
                        if nxt not in seen:
                            seen.add(nxt)
                            stack.append(nxt)
        return False
