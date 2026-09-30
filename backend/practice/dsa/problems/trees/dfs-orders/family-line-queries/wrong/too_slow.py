class Solution:
    # Climbs from b to the root for every query: O(depth) each, O(n * q) on a chain.
    def isAncestor(self, root, queries):
        parent = {root.val: None}
        todo = [root]
        while todo:
            node = todo.pop()
            for c in (node.left, node.right):
                if c:
                    parent[c.val] = node.val
                    todo.append(c)
        out = []
        for a, b in queries:
            cur = parent[b]
            while cur is not None and cur != a:
                cur = parent[cur]
            out.append(cur == a)
        return out
