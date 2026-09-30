class Solution:
    def shiftLine(self, head, k):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        if vals:
            for _ in range(k % len(vals)):
                vals.insert(0, vals.pop())
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
