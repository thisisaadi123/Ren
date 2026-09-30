class Solution:
    def foldChain(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        order, i, j = [], 0, len(vals) - 1
        while i <= j:
            order.append(vals[i])
            if i != j:
                order.append(vals[j])
            i += 1
            j -= 1
        out = None
        for v in reversed(order):
            out = ListNode(v, out)
        return out
