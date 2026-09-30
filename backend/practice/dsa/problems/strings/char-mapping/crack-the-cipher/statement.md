A spy intercepted one sentence in two forms: the original `plain` and the enciphered `coded`. The cipher replaces each letter with a fixed letter, different letters always with different letters (a letter may stand for itself), and leaves spaces alone.

Decode `message`, which uses the same cipher:
- A coded letter whose original you've learned becomes that original.
- If you've learned the originals of exactly 25 coded letters, the 26th coded letter is known too: it must stand for the one plain letter left over.
- Any other letter becomes `?`. Spaces stay spaces.

Return the decoded message.

{{examples}}

**Constraints**
- `1 ≤ plain.length = coded.length ≤ 10⁵`
- `1 ≤ message.length ≤ 10⁵`
- All three strings have lowercase English letters and spaces; `plain` and `coded` have spaces in exactly the same places.
- `plain` and `coded` agree with some one-to-one letter substitution.
