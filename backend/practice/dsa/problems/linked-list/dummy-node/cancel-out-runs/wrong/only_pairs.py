class Solution:
    # Mistake: only cancels a zero on its own or two neighbours that sum to zero.
    def cancelRuns(self, head):
        sheet = []
        while head:
            v = head.val
            if v == 0:
                pass
            elif sheet and sheet[-1] + v == 0:
                sheet.pop()
            else:
                sheet.append(v)
            head = head.next
        out = None
        for v in reversed(sheet):
            out = ListNode(v, out)
        return out
