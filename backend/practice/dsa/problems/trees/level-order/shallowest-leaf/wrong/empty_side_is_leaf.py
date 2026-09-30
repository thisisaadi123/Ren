class Solution:
    # Mistake: takes 1 + min(left, right) even when one side is empty, so a one-child node looks like a leaf.
    def shallowestLeaf(self, root):
        if not root:
            return 0
        best, stack = {}, [(root, False)]
        while stack:
            node, done = stack.pop()
            if done:
                best[node] = 1 + min(best.get(node.left, 0), best.get(node.right, 0))
            else:
                stack.append((node, True))
                for c in (node.left, node.right):
                    if c:
                        stack.append((c, False))
        return best[root]
