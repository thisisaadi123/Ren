class Solution:
    # Mistake: moves the left subtree over without reattaching the old right subtree.
    def flatten(self, root):
        cur = root
        while cur:
            if cur.left:
                cur.right = cur.left
                cur.left = None
            cur = cur.right
        return root
