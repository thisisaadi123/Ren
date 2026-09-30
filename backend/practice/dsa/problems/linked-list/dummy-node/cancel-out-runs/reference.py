class Solution:
    def cancelRuns(self, head):
        dummy = ListNode(0)
        last = dummy
        total = 0
        node_at = {0: dummy}    # running total -> kept node with that total
        total_of = {dummy: 0}   # kept node -> its running total
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
