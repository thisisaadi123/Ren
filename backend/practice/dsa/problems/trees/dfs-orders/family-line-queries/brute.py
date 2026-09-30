class Solution:
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
            cur, found = parent[b], False
            while cur is not None:
                if cur == a:
                    found = True
                    break
                cur = parent[cur]
            out.append(found)
        return out
