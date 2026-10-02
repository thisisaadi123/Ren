class Solution:
    # Mistake: only looks below the start node.
    def kAway(self, root, start, k):
        stack, node = [root], None
        while stack:
            n = stack.pop()
            if n.val == start:
                node = n
                break
            stack += [c for c in (n.left, n.right) if c]
        level = [node]
        for _ in range(k):
            level = [c for n in level for c in (n.left, n.right) if c]
        return sorted(n.val for n in level)
