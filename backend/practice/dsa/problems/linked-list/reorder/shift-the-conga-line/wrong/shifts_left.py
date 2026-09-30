class Solution:
    # Mistake: moves dancers from the front to the back instead.
    def shiftLine(self, head, k):
        if head is None:
            return None
        n, tail = 1, head
        while tail.next:
            tail = tail.next
            n += 1
        k %= n
        if k == 0:
            return head
        new_tail = head
        for _ in range(k - 1):
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None
        tail.next = head
        return new_head
