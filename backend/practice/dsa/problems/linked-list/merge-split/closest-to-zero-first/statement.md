A calibration log is a linked list of deviations from the target reading, starting at `head`; a deviation can be negative, zero or positive. The engineer wants to review them from the most accurate to the least accurate.

Sort the list by absolute value, smallest first. Deviations with the same absolute value (such as `-4`, `4` and another `-4`) must stay in the order they had in the log. Return the head of the sorted list.

{{examples}}

**Constraints**
- The list has between `0` and `5 × 10⁴` nodes.
- `-10⁹ ≤ node value ≤ 10⁹`
