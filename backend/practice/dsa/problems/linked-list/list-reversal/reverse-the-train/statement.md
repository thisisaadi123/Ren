A train is stored as a linked list: `head` is the engine, and each car points to the car behind it.

At the end of the line the train has to leave in the other direction. Reverse the list so the last car becomes the new head, and return that head.

{{examples}}

**Constraints**
- The train has between `0` and `10⁵` cars.
- `-10⁶ ≤ car value ≤ 10⁶`
