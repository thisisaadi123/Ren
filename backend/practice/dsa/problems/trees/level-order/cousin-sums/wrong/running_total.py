class Solution:
    # Mistake: re-reads the sibling pair after the left child has already been given its new value.
    def cousinSums(self, root):
        root.val = 0
        level = [root]
        while level:
            total, nxt = 0, []
            for n in level:
                total += sum(c.val for c in (n.left, n.right) if c)
            for n in level:
                for c in (n.left, n.right):
                    if c:
                        # the pair is re-read here, after the left sibling may already be overwritten
                        c.val = total - sum(k.val for k in (n.left, n.right) if k)
                        nxt.append(c)
            level = nxt
        return root
