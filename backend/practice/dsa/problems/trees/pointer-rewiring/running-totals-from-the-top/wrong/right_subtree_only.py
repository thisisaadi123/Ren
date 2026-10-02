class Solution:
    # Mistake: adds only the node's own right subtree, missing larger values above it.
    def totalsFromTop(self, root):
        def total(t):
            return 0 if not t else t.val + total(t.left) + total(t.right)

        sums, stack = [], [root]
        while stack:
            t = stack.pop()
            if t:
                sums.append((t, t.val + total(t.right)))
                stack += [t.left, t.right]
        for t, s in sums:
            t.val = s
        return root
