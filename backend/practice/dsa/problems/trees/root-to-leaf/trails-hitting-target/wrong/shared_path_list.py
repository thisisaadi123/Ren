class Solution:
    # Mistake: appends the live path list itself, which is emptied again by backtracking.
    def trailsWithSum(self, root, target):
        out, path = [], []

        def walk(node, left):
            path.append(node.val)
            left -= node.val
            if not node.left and not node.right:
                if left == 0:
                    out.append(path)
            else:
                if node.left:
                    walk(node.left, left)
                if node.right:
                    walk(node.right, left)
            path.pop()

        if root:
            walk(root, target)
        return out
