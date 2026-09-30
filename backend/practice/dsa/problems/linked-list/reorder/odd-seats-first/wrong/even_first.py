class Solution:
    # Mistake: serves the even seats first.
    def oddSeatsFirst(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        order = vals[1::2] + vals[0::2]
        out = None
        for v in reversed(order):
            out = ListNode(v, out)
        return out
