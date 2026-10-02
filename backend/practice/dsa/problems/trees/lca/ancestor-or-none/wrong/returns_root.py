class Solution:
    # Mistake: when both exist, returns the root instead of the lowest common node.
    def commonOrNone(self, root, p, q):
        seen, stack = set(), [root]
        while stack:
            n = stack.pop()
            seen.add(n.val)
            stack += [c for c in (n.left, n.right) if c]
        return root.val if p in seen and q in seen else -1
