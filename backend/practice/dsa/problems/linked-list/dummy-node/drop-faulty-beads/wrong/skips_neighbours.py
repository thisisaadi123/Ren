class Solution:
    # Mistake: always steps forward after a removal, so two faulty beads in a row leave one behind.
    def removeBeads(self, head, bad):
        dummy = ListNode(0, head)
        cur = dummy
        while cur and cur.next:
            if cur.next.val == bad:
                cur.next = cur.next.next
            cur = cur.next
        return dummy.next
