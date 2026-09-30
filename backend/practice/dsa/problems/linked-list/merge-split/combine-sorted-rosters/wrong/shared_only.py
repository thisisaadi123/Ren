class Solution:
    # Mistake: only skips a number when both fronts are equal; repeats inside one roster survive.
    def combineRosters(self, first, second):
        dummy = ListNode(0)
        tail = dummy
        while first and second:
            if first.val == second.val:
                tail.next = ListNode(first.val)
                first, second = first.next, second.next
            elif first.val < second.val:
                tail.next = ListNode(first.val)
                first = first.next
            else:
                tail.next = ListNode(second.val)
                second = second.next
            tail = tail.next
        tail.next = first or second
        return dummy.next
