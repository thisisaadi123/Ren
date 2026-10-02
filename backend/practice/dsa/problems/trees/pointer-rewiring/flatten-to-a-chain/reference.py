class Solution:
    def flatten(self, root):
        cur = root
        while cur:
            if cur.left:
                tail = cur.left
                while tail.right:
                    tail = tail.right
                tail.right = cur.right
                cur.right = cur.left
                cur.left = None
            cur = cur.right
        return root
