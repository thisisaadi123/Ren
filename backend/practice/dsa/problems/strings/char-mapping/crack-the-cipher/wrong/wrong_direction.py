class Solution:
    # Mistake: builds the plain → coded table and uses it on the coded message, which enciphers again.
    def crackCipher(self, plain, coded, message):
        fwd = {}
        for p, c in zip(plain, coded):
            if p != " ":
                fwd[p] = c
        if len(fwd) == 25:
            letters = "abcdefghijklmnopqrstuvwxyz"
            p = next(x for x in letters if x not in fwd)
            used = set(fwd.values())
            fwd[p] = next(x for x in letters if x not in used)
        fwd[" "] = " "
        return "".join(fwd.get(c, "?") for c in message)
