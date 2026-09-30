class Solution:
    # Mistake: flips the odd-sized groups instead of the even ones.
    def flipEvenGroups(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        out, i, size = [], 0, 1
        while i < len(vals):
            group = vals[i:i + size]
            out += group[::-1] if len(group) % 2 == 1 else group
            i += size
            size += 1
        res = None
        for v in reversed(out):
            res = ListNode(v, res)
        return res
