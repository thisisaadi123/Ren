class Solution:
    def twins(self, a, b):
        stack = [(a, b)]
        while stack:
            x, y = stack.pop()
            if not x and not y:
                continue
            if not x or not y or x.val != y.val:
                return False
            stack.append((x.left, y.left))
            stack.append((x.right, y.right))
        return True
