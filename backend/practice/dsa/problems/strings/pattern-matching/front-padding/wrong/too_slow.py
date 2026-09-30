class Solution:
    # Tests every prefix for being a palindrome: O(n^2) on "aaa...ab".
    def padToPalindrome(self, s):
        for k in range(len(s), -1, -1):
            i, j, ok = 0, k - 1, True
            while i < j:
                if s[i] != s[j]:
                    ok = False
                    break
                i += 1
                j -= 1
            if ok:
                return s[k:][::-1] + s
