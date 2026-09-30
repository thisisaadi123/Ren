class Solution:
    # Mistake: joins the two groups the wrong way round.
    def lowFirst(self, head, pivot):
        low, high = ListNode(0), ListNode(0)
        lt, ht = low, high
        while head:
            if head.val < pivot:
                lt.next = head
                lt = head
            else:
                ht.next = head
                ht = head
            head = head.next
        lt.next = None
        ht.next = low.next
        return high.next
