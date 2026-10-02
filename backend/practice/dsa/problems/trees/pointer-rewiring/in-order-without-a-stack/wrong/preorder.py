class Solution:
    # Mistake: records each node when first reaching it, which gives pre-order.
    def threadedInorder(self, root):
        out, cur = [], root
        while cur:
            if not cur.left:
                out.append(cur.val)
                cur = cur.right
                continue
            pred = cur.left
            while pred.right and pred.right is not cur:
                pred = pred.right
            if pred.right is None:
                out.append(cur.val)
                pred.right = cur
                cur = cur.left
            else:
                pred.right = None
                cur = cur.right
        return out
