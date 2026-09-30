class Solution:
    # Mistake: after visiting a node, pushes its right child but not that child's left chain.
    def guideSteps(self, root, ops):
        stack = []
        node = root
        while node:
            stack.append(node)
            node = node.left
        out = []
        for op in ops:
            if op == "hasNext":
                out.append(1 if stack else 0)
            else:
                cur = stack.pop()
                out.append(cur.val)
                if cur.right:
                    stack.append(cur.right)
        return out
