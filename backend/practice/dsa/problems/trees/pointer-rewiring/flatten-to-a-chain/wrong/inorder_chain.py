class Solution:
    # Mistake: chains the nodes in in-order instead of pre-order.
    def flatten(self, root):
        vals, stack, t = [], [], root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            vals.append(t.val)
            t = t.right
        head = None
        for v in reversed(vals):
            head = TreeNode(v, None, head)
        return head
