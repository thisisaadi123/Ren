class Solution:
    def hungryStudents(self, prefers, trays):
        want = [prefers.count(0), prefers.count(1)]
        for t in trays:
            if want[t] == 0:
                break
            want[t] -= 1
        return want[0] + want[1]
