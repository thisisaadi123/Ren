class Solution:
    def calendarsClash(self, a, b):
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i][0] < b[j][1] and b[j][0] < a[i][1]:
                return True
            if a[i][1] <= b[j][1]:
                i += 1
            else:
                j += 1
        return False
