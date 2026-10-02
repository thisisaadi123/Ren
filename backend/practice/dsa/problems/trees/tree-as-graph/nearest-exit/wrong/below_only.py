class Solution:
    # Mistake: only searches below the start node.
    def nearestExit(self, root, start):
        stack, node = [root], None
        while stack:
            n = stack.pop()
            if n.val == start:
                node = n
                break
            stack += [c for c in (n.left, n.right) if c]
        level = [node]
        while True:
            hits = [n.val for n in level if not n.left and not n.right]
            if hits:
                return min(hits)
            level = [c for n in level for c in (n.left, n.right) if c]
