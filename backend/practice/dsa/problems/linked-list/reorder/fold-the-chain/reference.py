class Solution:
    def foldChain(self, head):
        if head is None or head.next is None:
            return head
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        prev = None
        while second:
            second.next, prev, second = prev, second, second.next
        a, b = head, prev
        while b:
            an, bn = a.next, b.next
            a.next = b
            b.next = an
            a, b = an, bn
        return head
