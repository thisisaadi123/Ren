class Solution:
    def cousinSums(self, root):
        info = []  # (node, depth, parent id, original value)

        def walk(node, d, parent):
            if node:
                info.append((node, d, parent, node.val))
                walk(node.left, d + 1, id(node))
                walk(node.right, d + 1, id(node))

        walk(root, 0, None)
        new = [sum(v2 for _, d2, p2, v2 in info if d2 == d and p2 != p) for _, d, p, _ in info]
        for (node, _, _, _), v in zip(info, new):
            node.val = v
        return root
