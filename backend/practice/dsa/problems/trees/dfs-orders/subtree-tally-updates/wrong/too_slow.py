class Solution:
    # Walks the whole branch on every report: O(n) per report.
    def subtreeTotals(self, root, ops):
        nodes, todo = {}, [root]
        while todo:
            node = todo.pop()
            nodes[node.val] = node
            todo.extend(c for c in (node.left, node.right) if c)
        tally = dict.fromkeys(nodes, 0)
        out = []
        for op in ops:
            if op[0] == 1:
                tally[op[1]] += op[2]
            else:
                s, todo = 0, [nodes[op[1]]]
                while todo:
                    node = todo.pop()
                    s += tally[node.val]
                    todo.extend(c for c in (node.left, node.right) if c)
                out.append(s)
        return out
