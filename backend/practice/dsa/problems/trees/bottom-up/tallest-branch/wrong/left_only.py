class Solution:
    # Mistake: only follows the left side of the tree.
    def tallestBranch(self, root):
        n = 0
        while root:
            n += 1
            root = root.left
        return n
