class Solution:
    # Mistake: walks to the current tail for every fold step: O(n^2).
    def foldChain(self, head):
        cur = head
        while cur and cur.next and cur.next.next:
            prev = cur
            while prev.next.next:
                prev = prev.next
            last = prev.next
            prev.next = None
            last.next = cur.next
            cur.next = last
            cur = last.next
        return head
