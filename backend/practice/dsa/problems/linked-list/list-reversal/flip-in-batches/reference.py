class Solution:
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
            before.next = prev
            before = first
