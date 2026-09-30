class Solution:
    # Insertion sort on the list: O(n²).
    def sortCars(self, head):
        dummy = ListNode()
        while head:
            nxt = head.next
            prev = dummy
            while prev.next and prev.next.val < head.val:
                prev = prev.next
            head.next, prev.next = prev.next, head
            head = nxt
        return dummy.next
