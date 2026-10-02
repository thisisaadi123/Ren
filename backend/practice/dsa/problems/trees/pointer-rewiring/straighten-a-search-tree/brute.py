class Solution:
    def straighten(self, root):
        vals, stack = [], [root]
        while stack:
            n = stack.pop()
            if n:
                vals.append(n.val)
                stack += [n.left, n.right]
        head = None
        for v in sorted(vals, reverse=True):
            head = TreeNode(v, None, head)
        return head
