class Solution:
    # Mistake: adds up the SMALLER values, walking in normal in-order.
    def totalsFromTop(self, root):
        total, stack, t = 0, [], root
        while stack or t:
            while t:
                stack.append(t)
                t = t.left
            t = stack.pop()
            total += t.val
            t.val = total
            t = t.right
        return root
