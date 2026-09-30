class Solution:
    def zigzagFloors(self, root):
        floors = []

        def walk(node, d):
            if node:
                if d == len(floors):
                    floors.append([])
                floors[d].append(node.val)
                walk(node.left, d + 1)
                walk(node.right, d + 1)

        walk(root, 0)
        return [f if d % 2 == 0 else list(reversed(f)) for d, f in enumerate(floors)]
