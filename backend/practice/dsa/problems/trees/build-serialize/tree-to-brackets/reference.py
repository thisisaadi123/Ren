class Solution:
    def toBrackets(self, root):
        out = []
        stack = [root]
        while stack:
            item = stack.pop()
            if isinstance(item, str):
                out.append(item)
                continue
            out.append(str(item.val))
            if item.right:
                stack += [")", item.right, "("]
            if item.left:
                stack += [")", item.left, "("]
            elif item.right:
                stack.append("()")
        return "".join(out)
