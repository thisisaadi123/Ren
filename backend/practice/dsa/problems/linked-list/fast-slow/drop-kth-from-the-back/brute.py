class Solution:
    def dropFromBack(self, head, k):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        del vals[len(vals) - k]
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
