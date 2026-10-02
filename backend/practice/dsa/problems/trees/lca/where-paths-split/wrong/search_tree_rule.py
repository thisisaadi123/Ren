class Solution:
    # Mistake: steers by value as if the tree were a binary search tree.
    def splitPoint(self, root, p, q):
        node = root
        lo, hi = min(p, q), max(p, q)
        while node:
            if hi < node.val and node.left:
                node = node.left
            elif lo > node.val and node.right:
                node = node.right
            else:
                return node.val
        return root.val
