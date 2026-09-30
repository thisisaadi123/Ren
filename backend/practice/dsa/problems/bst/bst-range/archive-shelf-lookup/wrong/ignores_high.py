class Solution:
    # Mistake: forgets to check that the k-th id is still at most high.
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
            i = bisect.bisect_left(keys, low) + k - 1
            out.append(keys[i] if i < len(keys) else -1)
        return out
