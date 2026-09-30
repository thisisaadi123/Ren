class Solution:
    def mergeQueues(self, queues):
        vals = []
        for q in queues:
            while q:
                vals.append(q.val)
                q = q.next
        vals.sort()
        out = None
        for v in reversed(vals):
            out = ListNode(v, out)
        return out
