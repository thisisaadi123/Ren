class Solution:
    # Mistake: moves forward one node after each swap, so it keeps swapping overlapping pairs.
    def swapPartners(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            prev.next, a.next, b.next = b, b.next, a
            prev = b
        return dummy.next
