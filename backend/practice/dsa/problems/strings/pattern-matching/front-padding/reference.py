class Solution:
    def padToPalindrome(self, s):
        t = s + "#" + s[::-1]
        fail = [0] * len(t)
        k = 0
        for i in range(1, len(t)):
            while k and t[i] != t[k]:
                k = fail[k - 1]
            if t[i] == t[k]:
                k += 1
            fail[i] = k
        keep = fail[-1] if s else 0
        return s[keep:][::-1] + s
