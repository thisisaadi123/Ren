class Solution:
    def longestPath(self, root, target):
        first = {0: 0}
        best = 0
        stack = [(root, 0, 1, False, False)]
        while stack:
            node, s, d, leaving, added = stack.pop()
            if leaving:
                if added:
                    del first[s]
                continue
            s += node.val
            if s - target in first:
                best = max(best, d - first[s - target])
            added = s not in first
            if added:
                first[s] = d
            stack.append((node, s, d, True, added))
            for c in (node.right, node.left):
                if c:
                    stack.append((c, s, d + 1, False, False))
        return best
