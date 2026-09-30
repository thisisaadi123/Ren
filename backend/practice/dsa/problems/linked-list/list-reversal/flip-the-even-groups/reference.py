class Solution:
    def flipEvenGroups(self, head):
        dummy = ListNode(0, head)
        before = dummy
        size = 1
        while before.next:
            count, node = 0, before.next
            while node and count < size:
                node = node.next
                count += 1
            if count % 2 == 0:
                first = before.next
                prev, cur = node, first
                for _ in range(count):
                    cur.next, prev, cur = prev, cur, cur.next
                before.next = prev
                before = first
            else:
                for _ in range(count):
                    before = before.next
            size += 1
        return dummy.next
