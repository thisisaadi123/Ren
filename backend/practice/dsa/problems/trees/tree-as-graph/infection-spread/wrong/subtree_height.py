class Solution:
    # Mistake: only measures how deep the tree goes below the start node.
    def minutesToSpread(self, root, start):
        stack, node = [root], None
        while stack:
            n = stack.pop()
            if n.val == start:
                node = n
                break
            stack += [c for c in (n.left, n.right) if c]
        level, h = [node], -1
        while level:
            h += 1
            level = [c for n in level for c in (n.left, n.right) if c]
        return h
