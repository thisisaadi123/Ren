class Solution:
    # Mistake: links the nodes in order but never clears the left pointers.
    def straighten(self, root):
        order, stack, t = [], [], root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            order.append(t)
            t = t.right
        for a, b in zip(order, order[1:]):
            a.right = b
        order[-1].right = None
        return order[0]
