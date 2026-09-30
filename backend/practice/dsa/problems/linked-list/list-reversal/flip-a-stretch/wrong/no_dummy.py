class Solution:
    # Mistake: finds the node before `left` starting from the head, so left = 1 reverses from position 2.
    def flipStretch(self, head, left, right):
        before = head
        for _ in range(left - 2):
            before = before.next
        first = before.next
        if first is None:
            return head
        for _ in range(right - left):
            moved = first.next
            if moved is None:
                break
            first.next = moved.next
            moved.next = before.next
            before.next = moved
        return head
