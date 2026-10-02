class Solution:
    def cutRange(self, slots, cut):
        a, b = cut
        out = []
        for s, e in slots:
            left = [s, min(e, a)]
            right = [max(s, b), e]
            for piece in (left, right):
                if piece[0] < piece[1] and not (piece == left and piece == right):
                    if not out or out[-1] != piece:
                        out.append(piece)
        return out
