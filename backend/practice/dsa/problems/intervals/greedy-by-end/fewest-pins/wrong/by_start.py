class Solution:
    # Mistake: sorts by start and pins at the first poster's end without shrinking it.
    def fewestPins(self, posters):
        pins, at = 0, None
        for s, e in sorted(posters):
            if at is None or s > at:
                pins += 1
                at = e
        return pins
