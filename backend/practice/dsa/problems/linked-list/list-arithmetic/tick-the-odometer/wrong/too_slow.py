class Solution:
    # Mistake: walks from the head to each position from the back: O(n^2) on a run of 9s.
    def tick(self, head):
        n = 0
        node = head
        while node:
            n += 1
            node = node.next

        def at(i):
            node = head
            for _ in range(i):
                node = node.next
            return node

        i = n - 1
        while i >= 0 and at(i).val == 9:
            at(i).val = 0
            i -= 1
        if i < 0:
            return ListNode(1, head)
        at(i).val += 1
        return head
