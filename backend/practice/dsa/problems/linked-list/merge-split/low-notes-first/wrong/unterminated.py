class Solution:
    # Mistake: never cuts the high list's tail, which can still point back into the low list (a loop).
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
        lt.next = high.next
        return low.next
