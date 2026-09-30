class Solution:
    def insertSorted(self, head, value):
        dummy = ListNode(0, head)
        cur = dummy
        while cur.next and cur.next.val < value:
            cur = cur.next
        cur.next = ListNode(value, cur.next)
        return dummy.next
