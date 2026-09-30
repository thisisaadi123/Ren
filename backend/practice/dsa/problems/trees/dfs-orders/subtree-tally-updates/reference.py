class Solution:
    def subtreeTotals(self, root, ops):
        tin, tout = {}, {}
        clock = 0
        stack = [(root, False)]
        while stack:
            node, done = stack.pop()
            if done:
                tout[node.val] = clock
                continue
            clock += 1
            tin[node.val] = clock
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
        n = clock
        bit = [0] * (n + 1)

        def prefix(i):
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s

        out = []
        for op in ops:
            if op[0] == 1:
                i, x = tin[op[1]], op[2]
                while i <= n:
                    bit[i] += x
                    i += i & -i
            else:
                v = op[1]
                out.append(prefix(tout[v]) - prefix(tin[v] - 1))
        return out
