class Solution:
    def oddSeatsFirst(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        order = vals[0::2] + vals[1::2]
        out = None
        for v in reversed(order):
            out = ListNode(v, out)
        return out
