class Solution:
    def fromBrackets(self, s):
        stack, root, i = [], None, 0
        left_done = set()  # nodes whose left slot is filled or marked empty by "()"
        while i < len(s):
            c = s[i]
            if c == "(":
                if s[i + 1] == ")":
                    left_done.add(id(stack[-1]))
                    i += 2
                    continue
                i += 1
            elif c == ")":
                stack.pop()
                i += 1
            else:
                j = i + 1
                while j < len(s) and s[j].isdigit():
                    j += 1
                node = TreeNode(int(s[i:j]))
                if stack:
                    top = stack[-1]
                    if id(top) not in left_done:
                        top.left = node
                        left_done.add(id(top))
                    else:
                        top.right = node
                else:
                    root = node
                stack.append(node)
                i = j
        return root
