class Solution:
    # Mistake: measures the far-right edge and forgets the partly filled last floor.
    def countNodes(self, root):
        h = 0
        while root:
            h += 1
            root = root.right
        return (1 << h) - 1
