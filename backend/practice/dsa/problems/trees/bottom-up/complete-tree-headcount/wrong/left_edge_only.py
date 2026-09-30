class Solution:
    # Mistake: measures the far-left edge and assumes the tree is perfect.
    def countNodes(self, root):
        h = 0
        while root:
            h += 1
            root = root.left
        return (1 << h) - 1
