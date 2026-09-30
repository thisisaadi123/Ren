class Solution:
    # Mistake: counts visits against n with <=, so hasNext still says 1 after the last exhibit.
    def guideSteps(self, root, ops):
        seq, stack, node = [], [], root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            seq.append(node.val)
            node = node.right
        out, i = [], 0
        for op in ops:
            if op == "next":
                out.append(seq[i])
                i += 1
            else:
                out.append(1 if i <= len(seq) - 1 or i == len(seq) else 0)
        return out
