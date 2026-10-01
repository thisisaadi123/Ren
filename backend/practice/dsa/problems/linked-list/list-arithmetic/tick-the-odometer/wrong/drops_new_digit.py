class Solution:
    # Mistake: when every digit is 9, returns all zeros without the new leading 1.
    def tick(self, head):
        last = None
        node = head
        while node:
            if node.val != 9:
                last = node
            node = node.next
        if last:
            last.val += 1
            node = last.next
        else:
            node = head
        while node:
            node.val = 0
            node = node.next
        return head
