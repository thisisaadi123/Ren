class Solution:
    # Mistake: sums positions tin..tout-1, dropping the last office of the branch.
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
            for c in (node.right, node.left):
                if c:
                    stack.append((c, False))
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
                i = tin[op[1]]
                while i <= n:
                    bit[i] += op[2]
                    i += i & -i
            else:
                v = op[1]
                hi = tout[v] - 1 if tout[v] > tin[v] else tout[v]
                out.append(prefix(hi) - prefix(tin[v] - 1))
        return out
