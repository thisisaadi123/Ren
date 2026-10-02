class Solution:
    # Mistake: takes the first word that fits and never tries the others.
    def everySentence(self, text, words):
        ws = sorted(words)
        out, i = [], 0
        while i < len(text):
            w = next((w for w in ws if text.startswith(w, i)), None)
            if w is None:
                return []
            out.append(w)
            i += len(w)
        return [" ".join(out)]
