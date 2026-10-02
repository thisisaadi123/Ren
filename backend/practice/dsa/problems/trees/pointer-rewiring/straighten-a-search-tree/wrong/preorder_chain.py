class Solution:
    # Mistake: chains the nodes in pre-order, which isn't sorted.
    def straighten(self, root):
        dummy = last = TreeNode(0)
        stack = [root]
        while stack:
            n = stack.pop()
            if n:
                stack += [n.right, n.left]
                n.left = n.right = None
                last.right = n
                last = n
        return dummy.right
