class Solution:
    # Mistake: remembers the DEEPEST depth of each prefix, which finds the shortest path instead.
    def longestPath(self, root, target):
        last = {0: [0]}
        best = 0
        stack = [(root, 0, 1, False)]
        while stack:
            node, s, d, leaving = stack.pop()
            if leaving:
                last[s].pop()
                if not last[s]:
                    del last[s]
                continue
            s += node.val
            if s - target in last:
                best = max(best, d - last[s - target][-1])
            last.setdefault(s, []).append(d)
            stack.append((node, s, d, True))
            for c in (node.right, node.left):
                if c:
                    stack.append((c, s, d + 1, False))
        return best
