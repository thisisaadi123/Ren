class Solution:
    # Mistake: doesn't special-case k mod n == 0, so a whole number of turns cuts the line after the tail.
    def shiftLine(self, head, k):
        if head is None:
            return None
        n, tail = 1, head
        while tail.next:
            tail = tail.next
            n += 1
        k %= n
        new_tail = head
        for _ in range(n - k - 1):
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None
        tail.next = head
        return new_head
