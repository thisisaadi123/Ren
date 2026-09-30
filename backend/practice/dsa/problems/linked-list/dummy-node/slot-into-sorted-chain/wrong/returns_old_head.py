class Solution:
    # Mistake: returns the old head, so a value smaller than everything is lost.
    def insertSorted(self, head, value):
        dummy = ListNode(0, head)
        cur = dummy
        while cur.next and cur.next.val < value:
            cur = cur.next
        cur.next = ListNode(value, cur.next)
        return head if head else dummy.next
