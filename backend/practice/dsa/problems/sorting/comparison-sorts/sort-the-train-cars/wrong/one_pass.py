class Solution:
    # Mistake: swaps neighbours once instead of fully sorting.
    def sortCars(self, head):
        node = head
        while node and node.next:
            if node.val > node.next.val:
                node.val, node.next.val = node.next.val, node.val
            node = node.next
        return head
