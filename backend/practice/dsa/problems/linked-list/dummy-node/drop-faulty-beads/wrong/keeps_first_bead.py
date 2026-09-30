class Solution:
    # Mistake: no dummy node, so a faulty bead at the head is never checked.
    def removeBeads(self, head, bad):
        if head is None:
            return None
        cur = head
        while cur.next:
            if cur.next.val == bad:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head
