class Solution:
    def fromBrackets(self, s):
        def parse(i):
            j = i + 1 if s[i] == "-" else i
            while j < len(s) and s[j].isdigit():
                j += 1
            node = TreeNode(int(s[i:j]))
            i = j
            for side in ("left", "right"):
                if i < len(s) and s[i] == "(":
                    if s[i + 1] == ")":
                        i += 2
                        continue
                    child, i = parse(i + 1)
                    setattr(node, side, child)
                    i += 1  # the closing ")"
            return node, i

        return parse(0)[0]
