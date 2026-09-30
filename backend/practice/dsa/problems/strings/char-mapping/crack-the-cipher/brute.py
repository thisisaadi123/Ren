class Solution:
    def crackCipher(self, plain, coded, message):
        letters = "abcdefghijklmnopqrstuvwxyz"
        known_coded = set(coded) - {" "}
        known_plain = set(plain) - {" "}
        out = []
        for ch in message:
            if ch == " ":
                out.append(" ")
            elif ch in known_coded:
                out.append(plain[coded.index(ch)])
            elif len(known_coded) == 25:
                out.append([x for x in letters if x not in known_plain][0])
            else:
                out.append("?")
        return "".join(out)
