class Solution:
    def flipEquivalent(self, a, b):
        stack = [(a, b)]
        while stack:
            x, y = stack.pop()
            if not x and not y:
                continue
            if not x or not y or x.val != y.val:
                return False
            xl = x.left.val if x.left else None
            yl = y.left.val if y.left else None
            if xl == yl:
                stack.append((x.left, y.left))
                stack.append((x.right, y.right))
            else:
                stack.append((x.left, y.right))
                stack.append((x.right, y.left))
        return True
