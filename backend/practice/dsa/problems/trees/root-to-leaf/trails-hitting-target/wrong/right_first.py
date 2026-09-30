class Solution:
    # Mistake: explores right children first, so the routes come out in the wrong order.
    def trailsWithSum(self, root, target):
        out, path = [], []

        def walk(node, left):
            path.append(node.val)
            left -= node.val
            if not node.left and not node.right:
                if left == 0:
                    out.append(path[:])
            else:
                if node.right:
                    walk(node.right, left)
                if node.left:
                    walk(node.left, left)
            path.pop()

        if root:
            walk(root, target)
        return out
