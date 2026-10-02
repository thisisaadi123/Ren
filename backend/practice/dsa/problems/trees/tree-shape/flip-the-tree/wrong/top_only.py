class Solution:
    # Mistake: swaps only the root's children.
    def flip(self, root):
        if root:
            root.left, root.right = root.right, root.left
        return root
