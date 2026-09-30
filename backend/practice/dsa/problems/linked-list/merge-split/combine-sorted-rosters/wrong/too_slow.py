class Solution:
    # Mistake: inserts every number of the second roster by walking from the front: O(n * m).
    def combineRosters(self, first, second):
        dummy = ListNode(0)
        tail = dummy
        node = first
        while node:
            if tail is dummy or tail.val != node.val:
                tail.next = ListNode(node.val)
                tail = tail.next
            node = node.next
        node = second
        while node:
            prev = dummy
            while prev.next and prev.next.val < node.val:
                prev = prev.next
            if prev.next is None or prev.next.val != node.val:
                prev.next = ListNode(node.val, prev.next)
            node = node.next
        return dummy.next
