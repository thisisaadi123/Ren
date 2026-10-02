class Solution:
    def upsideDown(self, root):
        if not root or not root.left:
            return root
        left, right = root.left, root.right
        new_root = self.upsideDown(left)
        left.left, left.right = right, root
        root.left = root.right = None
        return new_root
