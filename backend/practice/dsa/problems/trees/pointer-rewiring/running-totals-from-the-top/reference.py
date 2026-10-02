class Solution:
    def totalsFromTop(self, root):
        total, cur = 0, root
        while cur:
            if not cur.right:
                total += cur.val
                cur.val = total
                cur = cur.left
                continue
            succ = cur.right
            while succ.left and succ.left is not cur:
                succ = succ.left
            if succ.left is None:
                succ.left = cur
                cur = cur.right
            else:
                succ.left = None
                total += cur.val
                cur.val = total
                cur = cur.left
        return root
