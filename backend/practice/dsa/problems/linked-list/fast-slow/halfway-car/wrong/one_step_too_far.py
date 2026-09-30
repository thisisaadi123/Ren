class Solution:
    # Mistake: moves slow even when fast has only one car left, overshooting on odd lengths.
    def halfwayCar(self, head):
        slow = fast = head
        while fast:
            slow = slow.next if slow.next else slow
            fast = fast.next.next if fast.next else None
        return slow
