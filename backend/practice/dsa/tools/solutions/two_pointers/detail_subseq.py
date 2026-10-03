"""In-depth text for the subsequence-matching problems (merged into their sol() calls via sol.EXTRA)."""
from sol import EXTRA, table

GREEDY = """
**Greedy matching is always safe.** To check whether `word` is hidden in `text`, read `text` left to right and match
the next needed letter of `word` the first time it appears. Why never wait for a later copy? Suppose some valid
matching uses a later copy of that letter. Swap in the earlier copy: the letters before it are unchanged, and
everything after it now has *more* text available, not less. So if any matching exists, the greedy one succeeds too.
"""


def hidden(w, t):
    i = 0
    for c in t:
        if i < len(w) and c == w[i]:
            i += 1
    return i == len(w)


# ---------------------------------------------------------------- hidden-word
word, text = "rent", "riverbend fountain"
hrows, i = [], 0
for p, c in enumerate(text):
    if i < len(word) and c == word[i]:
        hrows.append((p, repr(c), f"matches word[{i}] = '{word[i]}'", i + 1))
        i += 1
EXTRA["hidden-word"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - An empty word is hidden in any text (even an empty one).
        - A word longer than the text can't be hidden.
        - Repeated letters in the word need separate matches, in order (`"ee"` needs two `e`s).
        """
    ],
    "think": [
        GREEDY,
        f"**Matches for `\"{word}\"` in `\"{text}\"`** (only the positions that match are shown):",
        table(["text position", "char", "match", "letters matched"], *hrows),
        f"All {len(word)} letters matched: **true**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Keep `i`, the number of word letters matched so far. Read the text; whenever the current character equals
                `word[i]`, advance `i`. At the end, the word is hidden exactly when `i` reached its length.

                **Invariant.** After reading a prefix of the text, `i` is the longest prefix of `word` that is a
                subsequence of that text prefix (by the greedy argument).
                """
            ],
            "build": ["`i = 0`.", "For each text character, advance `i` on a match.", "Hidden if `i = len(word)`."],
            "complexity": ["**Time O(|text|).** **Space O(1).**"],
            "lines": {
                "init": "No letters of the word matched yet.",
                "scan": "Read the text once, left to right.",
                "match": "The next needed letter appears: take it immediately (greedy is optimal). The `i < len(word)` check stops matching once the word is complete.",
                "ret": "Every letter was matched in order.",
            },
        },
    },
    "takeaways": [
        """
        - **Subsequence check:** one pointer in the word, one pass over the text, greedy matches.
        - The exchange argument (an earlier match never hurts) justifies the greedy.
        - **Pitfall:** resetting the word pointer on a mismatch; that's substring matching, not subsequence.
        """
    ],
}


# ---------------------------------------------------------------- count-hidden-words
ct, cw = "trainstation", ["tin", "rain", "sat", "ran", "tin", "zoo"]
waiting = {}
for w in cw:
    waiting.setdefault(w[0], []).append((w, 0))
crows, done = [], 0
for c in ct:
    bucket = waiting.pop(c, [])
    moved = []
    for w, i in bucket:
        i += 1
        if i == len(w):
            done += 1
            moved.append(f"{w} done")
        else:
            waiting.setdefault(w[i], []).append((w, i))
            moved.append(f"{w}→waits for {w[i]}")
    if bucket:
        crows.append((repr(c), "; ".join(moved), done))
EXTRA["count-hidden-words"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - Repeated words count every time they appear in the list.
        - Words with letters missing from the text are never hidden.
        - Total work matters: up to 5000 words × 5 × 10⁴ text characters if each word rescans the text.
        """
    ],
    "think": [
        GREEDY,
        """
        **The cost of checking words one by one.** Each check reads the whole text: `words × text` steps, up to
        2.5 × 10⁸.

        **Two faster ideas.**

        1. **Jump instead of scanning.** Store, for each letter, the sorted positions where it occurs in the text. To match
           the next letter of a word after position `at`, binary-search that letter's list for the first position
           `> at`. Each word costs `O(len · log |text|)`.
        2. **Read the text once for all words.** Each word is waiting for one specific next letter. Keep 26 buckets of
           words, grouped by the letter they're waiting for. When the text shows letter `c`, every word in bucket `c`
           advances one letter and moves to the bucket of its next letter (or is finished).
        """,
        f"**Buckets on text `\"{ct}\"`** with words {cw} (only characters that move someone are shown):",
        table(["text char", "what happens", "finished so far"], *crows),
        f"Hidden words: **{done}**.",
    ],
    "approaches": {
        0: {
            "idea": ["Run the greedy subsequence check for every word, each one reading the whole text."],
            "build": ["For each word, greedy check over the text.", "Count the hidden ones."],
            "complexity": ["**Time O(W · T)**, where W is the number of words and T the text length: up to 2.5 × 10⁸. **Space O(1).**"],
            "limits": ["Each word re-reads the whole text, even the long stretches with none of its letters."],
            "lines": {
                "init": "The number of hidden words.",
                "each": "Check each word separately (repeats included).",
                "check": "Greedy subsequence check: advance in the word whenever the text shows its next letter.",
                "ret": "How many words were hidden.",
            },
        },
        1: {
            "idea": [
                """
                Precompute, for every letter, the sorted list of its positions in the text. For each word, keep `at` = the
                text position of the last matched letter (start at −1). For the next letter, binary-search its position
                list for the first position `> at`; if there is none, the word isn't hidden.

                This is the greedy matching, but jumping straight to the next useful position.
                """
            ],
            "build": ["Position lists per letter.", "For each word, jump letter by letter with binary search.", "Count the words that finish."],
            "complexity": ["**Time O(T + L · log T)**, where L is the total length of all words. **Space O(T)** for the position lists."],
            "limits": ["Every letter of every word pays a binary search. Reading the text once with buckets makes each letter advance in O(1)."],
            "lines": {
                "index": "For each letter, the increasing list of positions where it occurs in the text.",
                "init": "The count of hidden words.",
                "each": "Each word, matched from text position −1.",
                "jump": "The next letter's first occurrence after the last match, by binary search. None means the word can't be completed.",
                "ret": "How many words were hidden.",
            },
        },
        2: {
            "idea": [
                """
                26 buckets; bucket `c` holds `(word, i)` pairs for words whose next needed letter is `c` (`word[i] = c`).
                Put every word in the bucket of its first letter. Read the text once: for character `c`, take out bucket
                `c`, advance each word in it, and put each into the bucket of its new next letter, or count it as finished.

                **Why emptying the bucket first matters.** A word whose next letter is also `c` (like `"ee"`) must not use
                the same text character twice; taking the bucket out before re-inserting means it waits for the *next*
                `c`.
                """
            ],
            "build": ["Buckets by first letter.", "For each text character, advance everyone waiting for it.", "Count finished words."],
            "complexity": ["**Time O(T + L):** each text character is read once and each word letter is advanced once. **Space O(W)** for the bucket entries."],
            "lines": {
                "init": "Every word starts waiting for its first letter.",
                "read": "Read the text once. Take out the bucket for this character, so words re-inserted into it wait for a later copy.",
                "advance": "Each waiting word matches this character: it either finishes or moves to the bucket of its next letter.",
                "ret": "How many words finished.",
            },
        },
    },
    "takeaways": [
        """
        - **Many subsequence checks against one text:** either index the text (positions + binary search) or process all words in one pass with waiting buckets.
        - Grouping items by "what they wait for next" turns many scans into one.
        - **Pitfall:** letting a word use the same text character twice.
        """
    ],
}


# ---------------------------------------------------------------- longest-word-by-deleting
lt, ld = "brazenpanda", ["band", "zebra", "bread", "brand", "apple", "zap"]
best, lrows = "", []
for w in ld:
    wins = len(w) > len(best) or (len(w) == len(best) and w < best)
    if not wins:
        lrows.append((w, "can't beat the current best: skip the check", "—", best or '""'))
        continue
    h = hidden(w, lt)
    if h:
        best = w
    lrows.append((w, "could win: check it", "yes" if h else "no", best or '""'))
EXTRA["longest-word-by-deleting"] = {
    "question_more": [
        """
        **Edge cases to keep in mind**

        - No word can be made: return the empty string.
        - Ties in length: the alphabetically smaller word wins.
        - A word longer than the text can never be made.
        """
    ],
    "think": [
        GREEDY,
        """
        **Two parts.** "Can I make this word by deleting letters?" is the subsequence check. "Which one to return?" is a
        preference order: longer first, then alphabetical. The two approaches differ only in how they avoid unnecessary
        checks.
        """,
        f"**Single pass over the dictionary for `\"{lt}\"`:**",
        table(["word", "decision", "hidden?", "best so far"], *lrows),
        f"Answer **`\"{best}\"`**.",
    ],
    "approaches": {
        0: {
            "idea": [
                """
                Sort the dictionary by (length descending, then alphabetically) and return the first word that's hidden in
                the text. Every word before the answer in that order is checked, and the answer itself; the rest is never
                looked at.
                """
            ],
            "build": ["Subsequence helper.", "Sort by preference.", "Return the first hidden word."],
            "complexity": ["**Time O(D log D · w + D · T)** for D words of length up to w: sorting compares strings, and each check reads the text. **Space O(D)** for the sorted copy."],
            "limits": ["The sort costs extra and needs a copy of the dictionary. A single pass that keeps the best word checks only words that could beat it."],
            "lines": {
                "check": "Greedy subsequence check of one word against the text.",
                "order": "Longest first; among equal lengths, alphabetical.",
                "first": "The first hidden word in preference order is the answer.",
                "ret": "No word can be made.",
            },
        },
        1: {
            "idea": [
                """
                Keep the best word so far. For each dictionary word, first ask whether it would **win** (longer, or equal
                length and alphabetically smaller); only then run the subsequence check, and replace the best if it's
                hidden.

                **Why it's correct.** The final best is hidden, and every other hidden word was either checked and lost,
                or skipped because it couldn't beat a hidden word.
                """
            ],
            "build": ["Subsequence helper.", "Best = empty.", "For each word: skip if it can't win; otherwise check and update."],
            "complexity": ["**Time O(D · T)** in the worst case, usually much less because losing words aren't checked. **Space O(1)** besides the input."],
            "lines": {
                "check": "Greedy subsequence check of one word against the text.",
                "init": "The best word so far (empty means none).",
                "each": "Every dictionary word, in any order.",
                "wins": "Check only words that would beat the current best; then replace it if the word is hidden.",
                "ret": "The longest (then alphabetically first) word that can be made.",
            },
        },
    },
    "takeaways": [
        """
        - **Subsequence check + a preference order:** prune candidates that can't win before checking them.
        - Express the preference as a comparison (`(−length, word)`).
        - **Pitfall:** returning the first hidden word in input order instead of the preferred one.
        """
    ],
}
