class Solution:
    # Mistake: copies the list into a right-leaning chain: a search tree, but not balanced.
    def chainToTree(self, head):
        dummy = tail = TreeNode(0)
        while head:
            tail.right = TreeNode(head.val)
            tail = tail.right
            head = head.next
        return dummy.right
