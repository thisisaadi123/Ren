class Solution:
    # Mistake: finds the middle but compares the second half in its original order.
    def isMirrored(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        a, b = head, slow
        while b:
            if a.val != b.val:
                return False
            a, b = a.next, b.next
        return True
