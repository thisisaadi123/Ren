class Solution:
    # Mistake: ignores "()", so a right child after an empty left slot becomes a left child.
    def fromBrackets(self, s):
        stack, root, i = [], None, 0
        while i < len(s):
            c = s[i]
            if c == "(":
                i += 2 if s[i + 1] == ")" else 1
                continue
            if c == ")":
                stack.pop()
                i += 1
                continue
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            node = TreeNode(int(s[i:j]))
            if stack:
                top = stack[-1]
                if not top.left:
                    top.left = node
                else:
                    top.right = node
            else:
                root = node
            stack.append(node)
            i = j
        return root
