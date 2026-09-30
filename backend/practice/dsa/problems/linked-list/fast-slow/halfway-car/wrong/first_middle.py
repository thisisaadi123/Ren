class Solution:
    # Mistake: stops one step early, so an even list gives the first middle, not the second.
    def halfwayCar(self, head):
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow
