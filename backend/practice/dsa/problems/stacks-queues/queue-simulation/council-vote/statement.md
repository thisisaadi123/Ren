A council has two parties, the Larks (`L`) and the Owls (`O`). `council` lists the members in speaking order. Votes happen in rounds; in each round, every member who hasn't been silenced speaks in order and may do one thing:

- **Silence** one member of the other party. A silenced member loses every right from now on, in this round and all later ones.
- **Declare victory**, if every member still able to speak belongs to their own party.

Everyone plays as well as possible for their party. Return `"Larks"` or `"Owls"`, the party that declares victory.

{{examples}}

**Constraints**
- `1 ≤ council.length ≤ 10⁵`
- `council` has only the letters `L` and `O`.
