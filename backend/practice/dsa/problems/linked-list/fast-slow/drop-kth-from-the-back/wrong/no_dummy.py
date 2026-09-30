class Solution:
    # Mistake: starts at the head without a dummy, so removing the front node (k = n) goes wrong.
    def dropFromBack(self, head, k):
        lead = trail = head
        for _ in range(k):
            lead = lead.next
        if lead is None:
            trail.next = trail.next.next if trail.next else None
            return head if head.next else None
        while lead.next:
            lead = lead.next
            trail = trail.next
        trail.next = trail.next.next
        return head
