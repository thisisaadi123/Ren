class Solution:
    # Mistake: looks for a repeated value instead of a repeated node.
    def hasLoop(self, head):
        seen = set()
        while head:
            if head.val in seen:
                return True
            seen.add(head.val)
            head = head.next
        return False
