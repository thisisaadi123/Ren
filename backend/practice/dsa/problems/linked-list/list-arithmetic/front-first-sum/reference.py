class Solution:
    def addFrontFirst(self, a, b):
        x, y = [], []
        while a:
            x.append(a.val)
            a = a.next
        while b:
            y.append(b.val)
            b = b.next
        head = None
        carry = 0
        while x or y or carry:
            total = carry + (x.pop() if x else 0) + (y.pop() if y else 0)
            head = ListNode(total % 10, head)
            carry = total // 10
        return head
