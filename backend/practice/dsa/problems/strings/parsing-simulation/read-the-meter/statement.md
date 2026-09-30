A meter sends its reading as text, and you need the 32-bit integer at the front of it:

1. Skip any spaces at the start.
2. Read an optional `+` or `-` sign (at most one).
3. Read digits. A single `_` may sit **between two digits** as a separator; it's ignored. Stop at the first character that is neither a digit nor such a separator (a `_` that isn't followed by a digit stops the reading too).
4. If no digit was read, the reading is `0`. Otherwise apply the sign, and if the value is outside `[-2³¹, 2³¹ − 1]`, clamp it to the nearer end of that range.

Everything after the stopping point is ignored.

{{examples}}

**Constraints**
- `0 ≤ text.length ≤ 200`
- `text` has English letters, digits, spaces and the characters `+ - _ .`
