class Solution:
    # Mistake: partitions by swapping values like quicksort, which scrambles the order of the high group.
    def lowFirst(self, head, pivot):
        slot = head
        cur = head
        while cur:
            if cur.val < pivot:
                slot.val, cur.val = cur.val, slot.val
                slot = slot.next
            cur = cur.next
        return head
