class Solution:
    # Mistake: removes the k-th node from the front instead of from the back.
    def dropFromBack(self, head, k):
        dummy = ListNode(0, head)
        cur = dummy
        for _ in range(k - 1):
            cur = cur.next
        cur.next = cur.next.next
        return dummy.next
