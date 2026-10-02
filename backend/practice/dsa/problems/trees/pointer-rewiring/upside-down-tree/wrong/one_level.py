class Solution:
    # Mistake: only flips the top level.
    def upsideDown(self, root):
        if not root or not root.left:
            return root
        left, right = root.left, root.right
        left_kids = (left.left, left.right)
        left.left, left.right = right, root
        root.left = root.right = None
        if left_kids[0] or left_kids[1]:
            # The rest of the left edge is lost below the new root's old children.
            root.left, root.right = left_kids
        return left
