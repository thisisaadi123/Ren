class Solution:
    # Mistake: copies the left subtree to the right but leaves the left pointer set.
    def flatten(self, root):
        cur = root
        while cur:
            if cur.left:
                tail = cur.left
                while tail.right:
                    tail = tail.right
                tail.right = cur.right
                cur.right = cur.left
            cur = cur.right
        return root
