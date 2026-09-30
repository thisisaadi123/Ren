class Solution:
    # Mistake: reverses the whole list in place, then compares it with the old head,
    # which is now the tail, so only the first and last digits are compared.
    def isMirrored(self, head):
        prev, cur = None, head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        a, b = head, prev
        while a and b:
            if a.val != b.val:
                return False
            a, b = a.next, b.next
        return True
