class Solution:
    def isMirror(self, root):
        stack = [(root.left, root.right)]
        while stack:
            x, y = stack.pop()
            if not x and not y:
                continue
            if not x or not y or x.val != y.val:
                return False
            stack.append((x.left, y.right))
            stack.append((x.right, y.left))
        return True
