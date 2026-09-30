class Solution:
    # Mistake: the swapped pair's second node points to nothing, so an unpaired last dancer is lost.
    def swapPartners(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next and prev.next.next:
            a, b = prev.next, prev.next.next
            rest = b.next
            prev.next, b.next = b, a
            a.next = rest if rest and rest.next else None
            prev = a
        return dummy.next
