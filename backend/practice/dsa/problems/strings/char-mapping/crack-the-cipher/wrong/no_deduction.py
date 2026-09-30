class Solution:
    # Mistake: never deduces the 26th letter when 25 are known.
    def crackCipher(self, plain, coded, message):
        back = {" ": " "}
        for p, c in zip(plain, coded):
            back[c] = p
        return "".join(back.get(c, "?") for c in message)
