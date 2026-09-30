class Solution:
    def dropFromBack(self, head, k):
        dummy = ListNode(0, head)
        lead = trail = dummy
        for _ in range(k):
            lead = lead.next
        while lead.next:
            lead = lead.next
            trail = trail.next
        trail.next = trail.next.next
        return dummy.next
