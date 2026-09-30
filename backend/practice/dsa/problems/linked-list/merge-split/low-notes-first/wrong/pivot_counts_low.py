class Solution:
    # Mistake: puts values equal to the pivot in the low group.
    def lowFirst(self, head, pivot):
        low, high = ListNode(0), ListNode(0)
        lt, ht = low, high
        while head:
            if head.val <= pivot:
                lt.next = head
                lt = head
            else:
                ht.next = head
                ht = head
            head = head.next
        ht.next = None
        lt.next = high.next
        return low.next
