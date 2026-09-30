class Solution:
    # Mistake: the map doesn't start with total 0, so runs that begin at the front never cancel.
    def cancelRuns(self, head):
        dummy = ListNode(0)
        last = dummy
        total = 0
        node_at = {}
        total_of = {}
        cur = head
        while cur:
            nxt = cur.next
            total += cur.val
            anchor = node_at.get(total)
            if anchor is not None:
                gone = anchor.next
                while gone:
                    del node_at[total_of.pop(gone)]
                    gone = gone.next
                anchor.next = None
                last = anchor
            else:
                cur.next = None
                last.next = cur
                last = cur
                node_at[total] = cur
                total_of[cur] = total
            cur = nxt
        return dummy.next
