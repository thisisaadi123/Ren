class Solution:
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
                node = cur.right
                while node:
                    stack.append(node)
                    node = node.left
        return out
