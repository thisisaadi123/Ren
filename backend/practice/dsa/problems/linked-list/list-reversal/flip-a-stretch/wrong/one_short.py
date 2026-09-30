class Solution:
    # Mistake: moves one node too few, so the last runner of the stretch stays put.
    def flipStretch(self, head, left, right):
        dummy = ListNode(0, head)
        before = dummy
        for _ in range(left - 1):
            before = before.next
        first = before.next
        for _ in range(right - left - 1):
            moved = first.next
            first.next = moved.next
            moved.next = before.next
            before.next = moved
        return dummy.next
