class Solution:
    # Mistake: links each flipped batch to the next batch's old head instead of its new head.
    def flipBatches(self, head, k):
        dummy = ListNode(0, head)
        before = dummy
        while True:
            probe = before
            for _ in range(k):
                probe = probe.next
                if probe is None:
                    return dummy.next
            after = probe.next
            first = before.next
            prev, cur = after, first
            while cur is not after:
                cur.next, prev, cur = prev, cur, cur.next
            if before is dummy:
                before.next = prev
            before = first
