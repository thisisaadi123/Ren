class Solution:
    # Mistake: accepts a match even when the node has MORE below it than the branch.
    def hasBranch(self, root, branch):
        def covers(a, b):
            if not b:
                return True
            if not a or a.val != b.val:
                return False
            return covers(a.left, b.left) and covers(a.right, b.right)

        stack = [root]
        while stack:
            node = stack.pop()
            if node:
                if covers(node, branch):
                    return True
                stack += [node.left, node.right]
        return False
