class Solution:
    # Mistake: takes either all even levels or all odd levels, nothing in between.
    def mostApples(self, root):
        sums, level = [0, 0], [root]
        d = 0
        while level:
            sums[d % 2] += sum(n.val for n in level)
            level = [c for n in level for c in (n.left, n.right) if c]
            d += 1
        return max(sums)
