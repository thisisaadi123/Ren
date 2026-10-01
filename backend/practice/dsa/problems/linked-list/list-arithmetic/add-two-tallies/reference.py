class Solution:
    def addTallies(self, a, b):
        dummy = tail = ListNode(0)
        carry = 0
        while a or b or carry:
            total = carry
            if a:
                total += a.val
                a = a.next
            if b:
                total += b.val
                b = b.next
            tail.next = ListNode(total % 10)
            tail = tail.next
            carry = total // 10
        return dummy.next
