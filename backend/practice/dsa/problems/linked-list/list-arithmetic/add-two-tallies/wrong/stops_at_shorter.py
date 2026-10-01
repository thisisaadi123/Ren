class Solution:
    # Mistake: stops as soon as the shorter list ends.
    def addTallies(self, a, b):
        dummy = tail = ListNode(0)
        carry = 0
        while a and b:
            total = carry + a.val + b.val
            tail.next = ListNode(total % 10)
            tail = tail.next
            carry = total // 10
            a, b = a.next, b.next
        if carry:
            tail.next = ListNode(carry)
        return dummy.next
