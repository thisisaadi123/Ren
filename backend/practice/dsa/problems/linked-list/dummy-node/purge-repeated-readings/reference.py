class Solution:
    def purgeRepeats(self, head):
        dummy = ListNode(0, head)
        prev, cur = dummy, head
        while cur:
            if cur.next and cur.next.val == cur.val:
                v = cur.val
                while cur and cur.val == v:
                    cur = cur.next
                prev.next = cur
            else:
                prev, cur = cur, cur.next
        return dummy.next
