class Solution:
    def subtreeTotals(self, root, ops):
        # Every add climbs to the root and adds to each ancestor's running total.
        parent, total = {root.val: None}, {}
        todo = [root]
        while todo:
            node = todo.pop()
            total[node.val] = 0
            for c in (node.left, node.right):
                if c:
                    parent[c.val] = node.val
                    todo.append(c)
        out = []
        for op in ops:
            if op[0] == 1:
                cur = op[1]
                while cur is not None:
                    total[cur] += op[2]
                    cur = parent[cur]
            else:
                out.append(total[op[1]])
        return out
