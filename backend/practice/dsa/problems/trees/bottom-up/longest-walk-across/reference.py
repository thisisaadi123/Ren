class Solution:
    def longestWalk(self, root):
        best = [0]

        def depth(node):
            if node is None:
                return 0
            l, r = depth(node.left), depth(node.right)
            best[0] = max(best[0], l + r)
            return 1 + max(l, r)

        depth(root)
        return best[0]
