class Solution:
    def mirrorTrails(self, root):
        def trails(node):
            if not node.left and not node.right:
                return [[node.val]]
            return [[node.val] + t for c in (node.left, node.right) if c for t in trails(c)]

        return sum(t == t[::-1] for t in trails(root))
