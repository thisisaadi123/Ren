class Solution:
    def hasBranch(self, root, branch):
        def same(x, y):
            stack = [(x, y)]
            while stack:
                a, b = stack.pop()
                if not a and not b:
                    continue
                if not a or not b or a.val != b.val:
                    return False
                stack.append((a.left, b.left))
                stack.append((a.right, b.right))
            return True

        stack = [root]
        while stack:
            node = stack.pop()
            if node:
                if node.val == branch.val and same(node, branch):
                    return True
                stack += [node.left, node.right]
        return False
