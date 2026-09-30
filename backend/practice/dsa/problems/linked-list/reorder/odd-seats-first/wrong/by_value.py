class Solution:
    # Mistake: groups by odd and even values instead of odd and even positions.
    def oddSeatsFirst(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        order = [v for v in vals if v % 2] + [v for v in vals if v % 2 == 0]
        out = None
        for v in reversed(order):
            out = ListNode(v, out)
        return out
