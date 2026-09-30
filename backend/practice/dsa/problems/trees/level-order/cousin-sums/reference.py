class Solution:
    def cousinSums(self, root):
        root.val = 0
        level = [root]
        while level:
            total = sum(c.val for n in level for c in (n.left, n.right) if c)
            nxt = []
            for n in level:
                pair = (n.left.val if n.left else 0) + (n.right.val if n.right else 0)
                for c in (n.left, n.right):
                    if c:
                        nxt.append((c, total - pair))
            for c, v in nxt:
                c.val = v
            level = [c for c, _ in nxt]
        return root
