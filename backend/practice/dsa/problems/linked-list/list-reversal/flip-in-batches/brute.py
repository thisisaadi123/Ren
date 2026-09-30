class Solution:
    def flipBatches(self, head, k):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        out = []
        for i in range(0, len(vals), k):
            chunk = vals[i:i + k]
            out += chunk[::-1] if len(chunk) == k else chunk
        res = None
        for v in reversed(out):
            res = ListNode(v, res)
        return res
