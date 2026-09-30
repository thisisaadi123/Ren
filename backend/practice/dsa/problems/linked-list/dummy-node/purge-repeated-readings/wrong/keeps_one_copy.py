class Solution:
    # Mistake: keeps one copy of each repeated reading instead of deleting them all.
    def purgeRepeats(self, head):
        cur = head
        while cur and cur.next:
            if cur.next.val == cur.val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head
