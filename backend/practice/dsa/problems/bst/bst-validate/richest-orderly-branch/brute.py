class Solution:
    def richestOrderlyBranch(self, root):
        def values_in_order(node, out):
            if node:
                values_in_order(node.left, out)
                out.append(node.val)
                values_in_order(node.right, out)
            return out

        best = None
        stack = [root]
        while stack:
            node = stack.pop()
            seq = values_in_order(node, [])
            if all(a < b for a, b in zip(seq, seq[1:])):
                best = sum(seq) if best is None else max(best, sum(seq))
            for c in (node.left, node.right):
                if c:
                    stack.append(c)
        return best
