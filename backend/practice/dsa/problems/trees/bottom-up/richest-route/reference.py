class Solution:
    def richestRoute(self, root):
        best = [root.val]

        def gain(node):
            if node is None:
                return 0
            l = max(0, gain(node.left))
            r = max(0, gain(node.right))
            best[0] = max(best[0], node.val + l + r)
            return node.val + max(l, r)

        gain(root)
        return best[0]
