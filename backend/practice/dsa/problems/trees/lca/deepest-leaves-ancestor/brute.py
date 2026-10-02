class Solution:
    def deepestAncestor(self, root):
        paths = []

        def walk(t, path):
            if t:
                path = path + [t.val]
                paths.append(path)
                walk(t.left, path)
                walk(t.right, path)

        walk(root, [])
        deepest = max(len(p) for p in paths)
        best = [p for p in paths if len(p) == deepest]
        i = 0
        while all(len(p) > i for p in best) and len({p[i] for p in best}) == 1:
            i += 1
        return best[0][i - 1]
