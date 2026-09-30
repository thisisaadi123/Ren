class Solution:
    def tallestBranch(self, root):
        # Level by level, so a very deep (list-like) tree can't overflow the stack.
        levels = 0
        level = [root] if root else []
        while level:
            levels += 1
            level = [c for node in level for c in (node.left, node.right) if c]
        return levels
