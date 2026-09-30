class Solution:
    # Mistake: sorts by the signed value instead of the distance from zero.
    def sortByDistance(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        vals.sort()
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
