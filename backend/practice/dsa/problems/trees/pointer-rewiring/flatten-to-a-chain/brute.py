class Solution:
    def flatten(self, root):
        vals = []

        def pre(t):
            if t:
                vals.append(t.val)
                pre(t.left)
                pre(t.right)

        pre(root)
        head = None
        for v in reversed(vals):
            head = TreeNode(v, None, head)
        return head
