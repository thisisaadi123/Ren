class Solution:
    def swapPartners(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        for i in range(0, len(vals) - 1, 2):
            vals[i], vals[i + 1] = vals[i + 1], vals[i]
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
