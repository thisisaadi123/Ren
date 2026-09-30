class Solution:
    def cancelRuns(self, head):
        sheet = []
        while head:
            sheet.append(head.val)
            s = 0
            for j in range(len(sheet) - 1, -1, -1):
                s += sheet[j]
                if s == 0:
                    del sheet[j:]
                    break
            head = head.next
        out = None
        for v in reversed(sheet):
            out = ListNode(v, out)
        return out
