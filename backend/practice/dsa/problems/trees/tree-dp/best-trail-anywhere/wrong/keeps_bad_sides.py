class Solution:
    # Mistake: always adds both sides, even when a side's best run is negative.
    def bestTrail(self, root):
        order, stack = [], [root]
        while stack:
            n = stack.pop()
            order.append(n)
            stack += [c for c in (n.left, n.right) if c]
        gain = {}
        best = root.val
        for n in reversed(order):
            gl = gain[id(n.left)] if n.left else 0
            gr = gain[id(n.right)] if n.right else 0
            best = max(best, n.val + gl + gr)
            gain[id(n)] = n.val + max(gl, gr)
        return best
