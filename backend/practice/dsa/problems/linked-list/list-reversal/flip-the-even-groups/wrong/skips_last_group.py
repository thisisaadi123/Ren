class Solution:
    # Mistake: never touches a short last group, even when it has an even number of nodes.
    def flipEvenGroups(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        out, i, size = [], 0, 1
        while i < len(vals):
            group = vals[i:i + size]
            full = len(group) == size
            out += group[::-1] if full and size % 2 == 0 else group
            i += size
            size += 1
        res = None
        for v in reversed(out):
            res = ListNode(v, res)
        return res
