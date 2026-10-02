class Solution {
    public RandomNode copyList(RandomNode head) {
        java.util.Map<RandomNode, RandomNode> copy = new java.util.IdentityHashMap<>();
        for (RandomNode n = head; n != null; n = n.next) copy.put(n, new RandomNode(n.val));
        for (RandomNode n = head; n != null; n = n.next) {
            copy.get(n).next = n.next == null ? null : copy.get(n.next);
            copy.get(n).random = n.random == null ? null : copy.get(n.random);
        }
        return head == null ? null : copy.get(head);
    }
}
