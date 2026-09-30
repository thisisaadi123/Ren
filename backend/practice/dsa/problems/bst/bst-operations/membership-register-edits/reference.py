class Solution:
    def applyEdits(self, root, ops):
        for kind, k in ops:
            root = self._insert(root, k) if kind == 1 else self._delete(root, k)
        return root

    def _insert(self, root, k):
        if root is None:
            return TreeNode(k)
        cur = root
        while cur.val != k:
            if k < cur.val:
                if cur.left is None:
                    cur.left = TreeNode(k)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = TreeNode(k)
                    break
                cur = cur.right
        return root

    def _delete(self, root, k):
        parent, cur = None, root
        while cur and cur.val != k:
            parent, cur = cur, (cur.left if k < cur.val else cur.right)
        if cur is None:
            return root
        if cur.left and cur.right:
            sp, s = cur, cur.right
            while s.left:
                sp, s = s, s.left
            cur.val = s.val
            if sp is cur:
                sp.right = s.right
            else:
                sp.left = s.right
            return root
        child = cur.left or cur.right
        if parent is None:
            return child
        if parent.left is cur:
            parent.left = child
        else:
            parent.right = child
        return root
