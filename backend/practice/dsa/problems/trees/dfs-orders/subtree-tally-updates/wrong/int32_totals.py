class Solution:
    # Mistake: keeps totals in 32-bit integers, so big tallies overflow.
    def subtreeTotals(self, root, ops):
        def wrap(x):
            return (x + 2**31) % 2**32 - 2**31

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
                s = wrap(s + bit[i])
                i -= i & -i
            return s

        out = []
        for op in ops:
            if op[0] == 1:
                i = tin[op[1]]
                while i <= n:
                    bit[i] = wrap(bit[i] + op[2])
                    i += i & -i
            else:
                out.append(wrap(prefix(tout[op[1]]) - prefix(tin[op[1]] - 1)))
        return out
