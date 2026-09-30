class Solution:
    def purgeRepeats(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        count = collections.Counter(vals)
        out = None
        for v in reversed(vals):
            if count[v] == 1:
                out = ListNode(v, out)
        return out
