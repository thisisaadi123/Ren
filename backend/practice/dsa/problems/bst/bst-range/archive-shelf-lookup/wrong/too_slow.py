class Solution:
    # Mistake: correct, but walks the tree in order from low for every query: O(height + k) each.
    def kthInBand(self, root, queries):
        out = []
        for low, high, k in queries:
            stack, node = [], root
            while node:
                if node.val >= low:
                    stack.append(node)
                    node = node.left
                else:
                    node = node.right
            ans = -1
            while stack:
                cur = stack.pop()
                if cur.val > high:
                    break
                k -= 1
                if k == 0:
                    ans = cur.val
                    break
                node = cur.right
                while node:
                    stack.append(node)
                    node = node.left
            out.append(ans)
        return out
