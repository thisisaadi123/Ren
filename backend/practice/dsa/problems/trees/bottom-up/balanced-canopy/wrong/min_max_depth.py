class Solution:
    # Mistake: checks that the shallowest and deepest empty spots differ by at most one (a stricter rule).
    def isBalanced(self, root):
        depths = []

        def walk(node, d):
            if node is None:
                depths.append(d)
                return
            walk(node.left, d + 1)
            walk(node.right, d + 1)

        walk(root, 0)
        return max(depths) - min(depths) <= 1
