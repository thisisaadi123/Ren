class Solution:
    def shallowestLeaf(self, root):
        best = [0]

        def walk(node, d):
            if not node.left and not node.right:
                best[0] = d if best[0] == 0 else min(best[0], d)
            for c in (node.left, node.right):
                if c:
                    walk(c, d + 1)

        if root:
            walk(root, 1)
        return best[0]
