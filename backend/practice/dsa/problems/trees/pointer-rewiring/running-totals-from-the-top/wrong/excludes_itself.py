class Solution:
    # Mistake: writes the sum of the larger values only, leaving out the node's own value.
    def totalsFromTop(self, root):
        total, stack, t = 0, [], root
        while stack or t:
            while t:
                stack.append(t)
                t = t.right
            t = stack.pop()
            old = t.val
            t.val = total
            total += old
            t = t.left
        return root
