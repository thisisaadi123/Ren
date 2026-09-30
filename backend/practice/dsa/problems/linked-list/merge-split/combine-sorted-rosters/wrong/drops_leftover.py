class Solution:
    # Mistake: stops as soon as one roster runs out and forgets the rest of the other.
    def combineRosters(self, first, second):
        dummy = ListNode(0)
        tail = dummy
        while first and second:
            if first.val <= second.val:
                v, first = first.val, first.next
            else:
                v, second = second.val, second.next
            if tail is dummy or tail.val != v:
                tail.next = ListNode(v)
                tail = tail.next
        return dummy.next
