class Solution:
    def rebuildLine(self, people):
        line = []
        for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
            line.insert(k, [h, k])
        return line
