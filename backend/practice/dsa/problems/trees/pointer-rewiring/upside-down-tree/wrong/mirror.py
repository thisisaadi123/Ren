class Solution:
    # Mistake: mirrors the tree left to right instead of turning it upside down.
    def upsideDown(self, root):
        stack = [root]
        while stack:
            n = stack.pop()
            if n:
                n.left, n.right = n.right, n.left
                stack += [n.left, n.right]
        return root
