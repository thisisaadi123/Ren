class Solution:
    # Mistake: starts at the head without a dummy, so a repeated run at the front survives.
    def purgeRepeats(self, head):
        if head is None:
            return None
        prev = head
        cur = head.next
        while cur:
            if cur.next and cur.next.val == cur.val:
                v = cur.val
                while cur and cur.val == v:
                    cur = cur.next
                prev.next = cur
            else:
                prev, cur = cur, cur.next
        return head
