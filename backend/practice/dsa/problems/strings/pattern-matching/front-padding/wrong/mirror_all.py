class Solution:
    # Mistake: always mirrors everything after the first letter, which is a palindrome but not the shortest.
    def padToPalindrome(self, s):
        return s[1:][::-1] + s
