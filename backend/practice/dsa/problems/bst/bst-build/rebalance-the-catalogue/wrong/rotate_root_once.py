class Solution:
    # Mistake: only rotates at the root, which isn't enough for a long chain.
    def rebalance(self, root):
        def height(node):
            h, level = 0, [node] if node else []
            while level:
                h += 1
                level = [c for x in level for c in (x.left, x.right) if c]
            return h

        hl, hr = height(root.left), height(root.right)
        if hr > hl + 1:
            new = root.right
            root.right = new.left
            new.left = root
            return new
        if hl > hr + 1:
            new = root.left
            root.left = new.right
            new.right = root
            return new
        return root
