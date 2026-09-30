class Solution:
    # Mistake: decides by the planned group size, so a short last group is flipped (or not) wrongly.
    def flipEvenGroups(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        out, i, size = [], 0, 1
        while i < len(vals):
            group = vals[i:i + size]
            out += group[::-1] if size % 2 == 0 else group
            i += size
            size += 1
        res = None
        for v in reversed(out):
            res = ListNode(v, res)
        return res
