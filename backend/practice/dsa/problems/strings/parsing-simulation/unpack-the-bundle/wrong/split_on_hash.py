class Solution:
    # Mistake: splits the bundle on "#", which breaks as soon as a string contains "#".
    def unpack(self, bundle):
        parts = bundle.split("#")
        out = []
        for k in range(1, len(parts)):
            prev = parts[k - 1]
            j = len(prev)
            while j > 0 and prev[j - 1].isdigit():
                j -= 1
            size = int(prev[j:])
            out.append(parts[k][:size])
        return out
