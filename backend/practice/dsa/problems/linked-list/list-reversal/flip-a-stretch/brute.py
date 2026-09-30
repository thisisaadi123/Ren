class Solution:
    def flipStretch(self, head, left, right):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        vals[left - 1:right] = vals[left - 1:right][::-1]
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
