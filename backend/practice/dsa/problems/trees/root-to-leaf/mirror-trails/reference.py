class Solution:
    def mirrorTrails(self, root):
        M, B = (1 << 61) - 1, 1000003
        count = 0
        stack = [(root, 0, 0, 1)]  # node, forward hash, backward hash, B^depth
        while stack:
            node, f, r, p = stack.pop()
            f = (f + node.val * p) % M
            r = (r * B + node.val) % M
            p = p * B % M
            if not node.left and not node.right:
                count += f == r
            for c in (node.left, node.right):
                if c:
                    stack.append((c, f, r, p))
        return count
