class Solution:
    # Mistake: attaches the rest of the longer list as it is, ignoring the carry into it.
    def addTallies(self, a, b):
        dummy = tail = ListNode(0)
        carry = 0
        while a and b:
            total = carry + a.val + b.val
            tail.next = ListNode(total % 10)
            tail = tail.next
            carry = total // 10
            a, b = a.next, b.next
        rest = a or b
        if rest:
            tail.next = rest
        elif carry:
            tail.next = ListNode(carry)
        return dummy.next
