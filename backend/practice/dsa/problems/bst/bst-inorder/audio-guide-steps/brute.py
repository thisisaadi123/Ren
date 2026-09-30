class Solution:
    def guideSteps(self, root, ops):
        seq = []

        def walk(node):
            if node:
                walk(node.left)
                seq.append(node.val)
                walk(node.right)

        walk(root)
        out, i = [], 0
        for op in ops:
            if op == "next":
                out.append(seq[i])
                i += 1
            else:
                out.append(1 if i < len(seq) else 0)
        return out
