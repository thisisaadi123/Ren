class Solution:
    # Mistake: weaves starting from the back half, so the last label comes first.
    def foldChain(self, head):
        vals = []
        while head:
            vals.append(head.val)
            head = head.next
        order, i, j = [], 0, len(vals) - 1
        while i <= j:
            order.append(vals[j])
            if i != j:
                order.append(vals[i])
            i += 1
            j -= 1
        out = None
        for v in reversed(order):
            out = ListNode(v, out)
        return out
