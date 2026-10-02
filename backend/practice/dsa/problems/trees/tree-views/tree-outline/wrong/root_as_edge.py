class Solution:
    # Mistake: when the root has no left child, walks the left edge down the right side instead of leaving it empty.
    def outline(self, root):
        leaf = lambda n: not n.left and not n.right
        if leaf(root):
            return [root.val]
        out = [root.val]
        node = root.left or root.right
        while node and not leaf(node):
            out.append(node.val)
            node = node.left or node.right
        stack = [c for c in (root.right, root.left) if c]
        while stack:
            n = stack.pop()
            if leaf(n):
                out.append(n.val)
            stack += [c for c in (n.right, n.left) if c]
        right, node = [], root.right
        while node and not leaf(node):
            right.append(node.val)
            node = node.right or node.left
        return out + right[::-1]
