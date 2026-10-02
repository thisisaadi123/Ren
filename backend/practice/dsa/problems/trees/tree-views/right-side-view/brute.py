class Solution:
    def rightView(self, root):
        seen = {}

        def walk(t, d):
            if t:
                seen[d] = t.val  # later visits are further right in pre-order (left first)
                walk(t.left, d + 1)
                walk(t.right, d + 1)

        walk(root, 0)
        return [seen[d] for d in range(len(seen))]
