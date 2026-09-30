class Solution:
    # Looks up every message letter by scanning coded from the start: O(|message| · |coded|).
    def crackCipher(self, plain, coded, message):
        letters = "abcdefghijklmnopqrstuvwxyz"
        known = set(coded) - {" "}
        spare = None
        if len(known) == 25:
            used = set(plain)
            spare = [x for x in letters if x not in used][0]
        out = []
        for ch in message:
            if ch == " ":
                out.append(" ")
                continue
            found = "?"
            for i in range(len(coded)):
                if coded[i] == ch:
                    found = plain[i]
                    break
            if found == "?" and spare is not None:
                found = spare
            out.append(found)
        return "".join(out)
