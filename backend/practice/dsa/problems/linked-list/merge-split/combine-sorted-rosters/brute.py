class Solution:
    def combineRosters(self, first, second):
        vals = set()
        for node in (first, second):
            while node:
                vals.add(node.val)
                node = node.next
        out = None
        for v in sorted(vals, reverse=True):
            out = ListNode(v, out)
        return out
