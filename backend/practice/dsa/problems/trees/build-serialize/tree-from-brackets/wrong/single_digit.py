class Solution:
    # Mistake: reads one digit per value and ignores minus signs.
    def fromBrackets(self, s):
        stack, root, done = [], None, set()
        i = 0
        while i < len(s):
            c = s[i]
            if c == "(" and s[i + 1] == ")":
                done.add(id(stack[-1]))
                i += 2
                continue
            if c == ")":
                stack.pop()
            elif c.isdigit():
                node = TreeNode(int(c))
                if stack:
                    top = stack[-1]
                    if id(top) not in done:
                        top.left = node
                        done.add(id(top))
                    else:
                        top.right = node
                else:
                    root = node
                stack.append(node)
            i += 1
        return root
