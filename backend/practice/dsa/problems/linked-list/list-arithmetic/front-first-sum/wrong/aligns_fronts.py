class Solution:
    # Mistake: lines the two numbers up at their first digits instead of their last.
    def addFrontFirst(self, a, b):
        x, y = [], []
        while a:
            x.append(a.val)
            a = a.next
        while b:
            y.append(b.val)
            b = b.next
        n = max(len(x), len(y))
        x += [0] * (n - len(x))
        y += [0] * (n - len(y))
        head = None
        carry = 0
        for i in range(n - 1, -1, -1):
            total = carry + x[i] + y[i]
            head = ListNode(total % 10, head)
            carry = total // 10
        if carry:
            head = ListNode(carry, head)
        return head
