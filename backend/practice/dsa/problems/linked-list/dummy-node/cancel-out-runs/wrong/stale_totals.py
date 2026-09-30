class Solution:
    # Mistake: never forgets the totals of crossed-out nodes, so later jumps land on removed nodes.
    def cancelRuns(self, head):
        dummy = ListNode(0)
        last = dummy
        total = 0
        node_at = {0: dummy}
        cur = head
        while cur:
            nxt = cur.next
            total += cur.val
            anchor = node_at.get(total)
            if anchor is not None:
                anchor.next = None
                last = anchor
            else:
                cur.next = None
                last.next = cur
                last = cur
                node_at[total] = cur
            cur = nxt
        return dummy.next
