class Solution:
    # Mistake: stops before nodes whose children are both leaves.
    def flip(self, root):
        def go(n):
            if not n or (not n.left and not n.right):
                return
            if (n.left is None or (not n.left.left and not n.left.right)) and (n.right is None or (not n.right.left and not n.right.right)):
                return
            n.left, n.right = n.right, n.left
            go(n.left)
            go(n.right)

        go(root)
        return root
