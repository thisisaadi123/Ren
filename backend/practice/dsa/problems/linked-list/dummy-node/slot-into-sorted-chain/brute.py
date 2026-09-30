class Solution:
    def insertSorted(self, head, value):
        vals = [value]
        while head:
            vals.append(head.val)
            head = head.next
        vals.sort()
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
