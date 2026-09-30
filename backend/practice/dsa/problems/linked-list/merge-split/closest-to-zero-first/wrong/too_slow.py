class Solution:
    # Mistake: insertion sort into a growing list, O(n^2) when the log is far-to-near.
    def sortByDistance(self, head):
        dummy = ListNode(0)
        while head:
            nxt = head.next
            prev = dummy
            while prev.next and abs(prev.next.val) <= abs(head.val):
                prev = prev.next
            head.next = prev.next
            prev.next = head
            head = nxt
        return dummy.next
