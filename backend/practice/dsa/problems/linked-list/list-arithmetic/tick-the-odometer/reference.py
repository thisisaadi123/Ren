class Solution:
    def tick(self, head):
        dummy = ListNode(0, head)
        last = dummy
        node = head
        while node:
            if node.val != 9:
                last = node
            node = node.next
        last.val += 1
        node = last.next
        while node:
            node.val = 0
            node = node.next
        return dummy if dummy.val else dummy.next
