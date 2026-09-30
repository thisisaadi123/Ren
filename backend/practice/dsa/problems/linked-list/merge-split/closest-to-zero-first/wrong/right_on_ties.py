class Solution:
    # Mistake: takes from the right half on ties, so equal distances lose their original order.
    def sortByDistance(self, head):
        if head is None or head.next is None:
            return head
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        right = slow.next
        slow.next = None
        a = self.sortByDistance(head)
        b = self.sortByDistance(right)
        dummy = ListNode(0)
        tail = dummy
        while a and b:
            if abs(a.val) < abs(b.val):
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next
