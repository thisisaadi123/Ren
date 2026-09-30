class Solution:
    # Mistake: after every node, re-adds the sheet from the end looking for a zero run: O(n^2).
    def cancelRuns(self, head):
        dummy = ListNode(0)
        cur = head
        while cur:
            nxt = cur.next
            cur.next = None
            last = dummy
            while last.next:
                last = last.next
            last.next = cur
            vals = []
            node = dummy.next
            while node:
                vals.append(node.val)
                node = node.next
            s = 0
            for j in range(len(vals) - 1, -1, -1):
                s += vals[j]
                if s == 0:
                    node = dummy
                    for _ in range(j):
                        node = node.next
                    node.next = None
                    break
            cur = nxt
        return dummy.next
