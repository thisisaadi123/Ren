class Solution:
    def lowFirst(self, head, pivot):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        order = [v for v in vals if v < pivot] + [v for v in vals if v >= pivot]
        out = None
        for v in reversed(order):
            out = ListNode(v, out)
        return out
