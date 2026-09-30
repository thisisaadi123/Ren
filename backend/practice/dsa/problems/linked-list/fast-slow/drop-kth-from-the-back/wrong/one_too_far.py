class Solution:
    # Mistake: moves until the leader falls off the end, so the trailer stops ON the target and removes the node after it.
    def dropFromBack(self, head, k):
        dummy = ListNode(0, head)
        lead = trail = dummy
        for _ in range(k):
            lead = lead.next
        while lead:
            lead = lead.next
            trail = trail.next
        if trail.next:
            trail.next = trail.next.next
        return dummy.next
