class Solution:
    def minInsertions(self, s):
        while "()" in s:
            s = s.replace("()", "")
        return len(s)
