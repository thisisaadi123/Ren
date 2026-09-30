class Solution:
    def crackCipher(self, plain, coded, message):
        back = {}
        for p, c in zip(plain, coded):
            if c != " ":
                back[c] = p
        if len(back) == 25:
            letters = "abcdefghijklmnopqrstuvwxyz"
            c = next(x for x in letters if x not in back)
            used = set(back.values())
            back[c] = next(x for x in letters if x not in used)
        back[" "] = " "
        return "".join(back.get(c, "?") for c in message)
