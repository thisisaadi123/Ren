class Solution:
    # Mistake: flips the first batch and forgets to continue with the rest of the list.
    def flipBatches(self, head, k):
        prev, cur = None, head
        for _ in range(k):
            cur.next, prev, cur = prev, cur, cur.next
        head.next = cur
        return prev
