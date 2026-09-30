class Solution:
    # Mistake: stops one car early, so the last car is lost.
    def reverseTrain(self, head):
        prev = None
        while head and head.next:
            head.next, prev, head = prev, head, head.next
        return prev
