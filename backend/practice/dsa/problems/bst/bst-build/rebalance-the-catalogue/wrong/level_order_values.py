class Solution:
    # Mistake: collects values level by level instead of in order, so the rebuilt tree isn't sorted.
    def rebalance(self, root):
        vals, queue = [], [root]
        for node in queue:
            vals.append(node.val)
            queue += [c for c in (node.left, node.right) if c]

        def build(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            return TreeNode(vals[mid], build(lo, mid - 1), build(mid + 1, hi))

        return build(0, len(vals) - 1)
