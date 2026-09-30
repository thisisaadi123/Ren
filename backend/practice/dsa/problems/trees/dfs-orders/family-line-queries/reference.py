class Solution:
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
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
        return [tin[a] < tin[b] <= tout[a] for a, b in queries]
