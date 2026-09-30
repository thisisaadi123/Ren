class Solution:
    # Copies the whole path at every leaf and sums it: O(n * height) on a comb-shaped map.
    def hasTrailSum(self, root, target):
        trails, path = [], []

        def walk(node):
            path.append(node.val)
            if not node.left and not node.right:
                trails.append(list(path))
            for c in (node.left, node.right):
                if c:
                    walk(c)
            path.pop()

        if root:
            walk(root)
        return any(sum(t) == target for t in trails)
