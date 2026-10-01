class Solution:
    def tick(self, head):
        digits = []
        while head:
            digits.append(head.val)
            head = head.next
        i = len(digits) - 1
        while i >= 0 and digits[i] == 9:
            digits[i] = 0
            i -= 1
        if i < 0:
            digits.insert(0, 1)
        else:
            digits[i] += 1
        out = None
        for d in reversed(digits):
            out = ListNode(d, out)
        return out
