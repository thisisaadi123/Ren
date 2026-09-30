class Solution:
    # Mistake: records a route as soon as the running total matches, even above a leaf.
    def trailsWithSum(self, root, target):
        out, path = [], []

        def walk(node, left):
            path.append(node.val)
            left -= node.val
            if left == 0:
                out.append(path[:])
            if node.left:
                walk(node.left, left)
            if node.right:
                walk(node.right, left)
            path.pop()

        if root:
            walk(root, target)
        return out
