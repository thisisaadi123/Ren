class Solution:
    # Mistake: starts the band after low, so an id equal to low is skipped.
    def kthInBand(self, root, queries):
        keys, stack, node = [], [], root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            keys.append(node.val)
            node = node.right
        out = []
        for low, high, k in queries:
            i = bisect.bisect_right(keys, low) + k - 1
            out.append(keys[i] if i < len(keys) and keys[i] <= high else -1)
        return out
