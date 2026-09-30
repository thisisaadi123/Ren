class Solution:
    # Mistake: weaves in the second half without reversing it first.
    def foldChain(self, head):
        if head is None or head.next is None:
            return head
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        a, b = head, second
        while b:
            an, bn = a.next, b.next
            a.next = b
            b.next = an
            a, b = an, bn
        return head
