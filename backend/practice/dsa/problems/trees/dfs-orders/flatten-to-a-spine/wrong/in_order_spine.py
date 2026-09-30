class Solution:
    # Mistake: lays the nodes out in in-order instead of pre-order.
    def flattenToSpine(self, root):
        order = []

        def walk(node):
            if node:
                walk(node.left)
                order.append(node)
                walk(node.right)

        walk(root)
        for a, b in zip(order, order[1:] + [None]):
            a.left, a.right = None, b
        return order[0] if order else None
