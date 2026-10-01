class Solution:
    # Mistake: appends each digit at the end, so the answer comes out ones digit first.
    def addFrontFirst(self, a, b):
        x, y = [], []
        while a:
            x.append(a.val)
            a = a.next
        while b:
            y.append(b.val)
            b = b.next
        dummy = tail = ListNode(0)
        carry = 0
        while x or y or carry:
            total = carry + (x.pop() if x else 0) + (y.pop() if y else 0)
            tail.next = ListNode(total % 10)
            tail = tail.next
            carry = total // 10
        return dummy.next
