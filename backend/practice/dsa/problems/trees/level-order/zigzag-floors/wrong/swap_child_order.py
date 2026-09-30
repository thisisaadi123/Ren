class Solution:
    # Mistake: on odd floors enqueues children right-first instead of reversing the floor,
    # which only flips siblings and scrambles deeper floors.
    def zigzagFloors(self, root):
        out, level = [], [root] if root else []
        while level:
            out.append([n.val for n in level])
            nxt = []
            for n in level:
                kids = (n.right, n.left) if len(out) % 2 else (n.left, n.right)
                nxt.extend(c for c in kids if c)
            level = nxt
        return out
