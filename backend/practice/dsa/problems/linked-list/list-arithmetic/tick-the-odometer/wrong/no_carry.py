class Solution:
    # Mistake: adds 1 to the last digit and never carries, so a 9 becomes 10.
    def tick(self, head):
        node = head
        while node.next:
            node = node.next
        node.val += 1
        return head
