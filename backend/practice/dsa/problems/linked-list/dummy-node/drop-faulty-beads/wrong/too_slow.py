class Solution:
    # Mistake: restarts from the head to find each faulty bead, O(n^2) when they sit at the end.
    def removeBeads(self, head, bad):
        dummy = ListNode(0, head)
        while True:
            cur = dummy
            while cur.next and cur.next.val != bad:
                cur = cur.next
            if cur.next is None:
                return dummy.next
            cur.next = cur.next.next
