class Solution:
    # Mistake: the bigger party always wins; ties go to whoever speaks first.
    def councilWinner(self, council):
        l, o = council.count("L"), council.count("O")
        if l != o:
            return "Larks" if l > o else "Owls"
        return "Larks" if council[0] == "L" else "Owls"
