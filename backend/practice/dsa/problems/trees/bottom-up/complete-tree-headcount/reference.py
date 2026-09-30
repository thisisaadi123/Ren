class Solution:
    def countNodes(self, root):
        def count(node):
            if node is None:
                return 0
            lh, x = 0, node
            while x:
                lh += 1
                x = x.left
            rh, x = 0, node
            while x:
                rh += 1
                x = x.right
            if lh == rh:
                return (1 << lh) - 1
            return 1 + count(node.left) + count(node.right)

        return count(root)
