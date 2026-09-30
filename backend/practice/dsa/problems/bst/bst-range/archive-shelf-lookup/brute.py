class Solution:
    def kthInBand(self, root, queries):
        vals, stack = [], [root]
        while stack:
            node = stack.pop()
            if node:
                vals.append(node.val)
                stack.append(node.left)
                stack.append(node.right)
        out = []
        for low, high, k in queries:
            band = sorted(v for v in vals if low <= v <= high)
            out.append(band[k - 1] if k <= len(band) else -1)
        return out
