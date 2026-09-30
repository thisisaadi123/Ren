class Solution:
    # Mistake: also flips the final batch when it has fewer than k crates.
    def flipBatches(self, head, k):
        dummy = ListNode(0, head)
        before = dummy
        while before.next:
            probe = before
            for _ in range(k):
                if probe.next is None:
                    break
                probe = probe.next
            after = probe.next
            first = before.next
            prev, cur = after, first
            while cur is not after:
                cur.next, prev, cur = prev, cur, cur.next
            before.next = prev
            before = first
        return dummy.next
