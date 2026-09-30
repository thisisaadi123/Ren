class Solution:
    # Mistake: removes a node and its twin, so a run of three leaves one copy behind.
    def purgeRepeats(self, head):
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next:
            cur = prev.next
            if cur.next and cur.next.val == cur.val:
                prev.next = cur.next.next
            else:
                prev = cur
        return dummy.next
