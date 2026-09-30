class Solution:
    def removeBeads(self, head, bad):
        dummy = ListNode(0, head)
        cur = dummy
        while cur.next:
            if cur.next.val == bad:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return dummy.next
