class Solution:
    # Compares each trail with its reverse from scratch: O(n * height) on a comb.
    def mirrorTrails(self, root):
        count, path = 0, []
        stack = [(root, 0)]
        while stack:
            node, d = stack.pop()
            del path[d:]
            path.append(node.val)
            if not node.left and not node.right:
                count += path == path[::-1]
            for c in (node.left, node.right):
                if c:
                    stack.append((c, d + 1))
        return count
