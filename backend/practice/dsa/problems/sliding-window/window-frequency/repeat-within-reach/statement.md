A scanner reads product codes `codes` in order. Return `true` if the same code shows up twice **at most `k` positions apart**: that is, there are indexes `i < j` with `codes[i] == codes[j]` and `j − i ≤ k`. Otherwise return `false`.

{{examples}}

**Constraints**
- `1 ≤ codes.length ≤ 10⁵`
- `-10⁹ ≤ codes[i] ≤ 10⁹`
- `0 ≤ k ≤ 10⁵`
