class Solution:
    # Mistake: only compares entry times, so any node visited earlier looks like an ancestor.
    def isAncestor(self, root, queries):
        tin = {}
        stack = [root]
        while stack:
            node = stack.pop()
            tin[node.val] = len(tin)
            for c in (node.right, node.left):
                if c:
                    stack.append(c)
        return [tin[a] < tin[b] for a, b in queries]
