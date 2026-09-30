class Solution:
    # Mistake: treats a person as their own ancestor.
    def isAncestor(self, root, queries):
        tin, tout = {}, {}
        clock = 0
        stack = [(root, False)]
        while stack:
            node, done = stack.pop()
            if done:
                tout[node.val] = clock - 1
                continue
            tin[node.val] = clock
            clock += 1
            stack.append((node, True))
            for c in (node.right, node.left):
                if c:
                    stack.append((c, False))
        return [tin[a] <= tin[b] <= tout[a] for a, b in queries]
