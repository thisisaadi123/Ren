class Solution:
    # Mistake: never goes back up, so only the leftmost path and right branches below it are visited.
    def threadedInorder(self, root):
        out, cur = [], root
        while cur and cur.left:
            cur = cur.left
        while cur:
            out.append(cur.val)
            cur = cur.right
        return out
