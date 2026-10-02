class Solution:
    # Mistake: never forgets prefixes from finished branches.
    def longestPath(self, root, target):
        first = {0: 0}
        best = 0
        stack = [(root, 0, 1)]
        while stack:
            node, s, d = stack.pop()
            s += node.val
            if s - target in first and first[s - target] < d:
                best = max(best, d - first[s - target])
            first.setdefault(s, d)
            for c in (node.right, node.left):
                if c:
                    stack.append((c, s, d + 1))
        return best
