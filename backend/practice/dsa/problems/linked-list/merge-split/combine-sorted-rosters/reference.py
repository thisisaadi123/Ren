class Solution:
    def combineRosters(self, first, second):
        dummy = ListNode(0)
        tail = dummy
        while first or second:
            if second is None or (first is not None and first.val <= second.val):
                v, first = first.val, first.next
            else:
                v, second = second.val, second.next
            if tail is dummy or tail.val != v:
                tail.next = ListNode(v)
                tail = tail.next
        return dummy.next
