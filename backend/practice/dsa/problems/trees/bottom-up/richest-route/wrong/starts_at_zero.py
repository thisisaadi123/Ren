class Solution:
    # Mistake: starts the best total at 0, which is wrong when every cave is negative.
    def richestRoute(self, root):
        best = [0]

        def gain(node):
            if node is None:
                return 0
            l = max(0, gain(node.left))
            r = max(0, gain(node.right))
            best[0] = max(best[0], node.val + l + r)
            return node.val + max(l, r)

        gain(root)
        return best[0]
