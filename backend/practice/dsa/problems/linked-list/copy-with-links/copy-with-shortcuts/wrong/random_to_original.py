class Solution:
    # Mistake: copies the next chain but points random at the ORIGINAL nodes.
    def copyList(self, head):
        dummy = tail = RandomNode(0)
        node = head
        while node:
            tail.next = RandomNode(node.val, None, node.random)
            tail = tail.next
            node = node.next
        return dummy.next
