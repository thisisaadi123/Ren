/* Weave each copy right after its original, set the shortcuts, then unweave. */
struct RandomNode* copyList(struct RandomNode* head) {
    for (struct RandomNode* n = head; n; n = n->next->next) {
        struct RandomNode* c = malloc(sizeof(struct RandomNode));
        c->val = n->val;
        c->next = n->next;
        c->random = NULL;
        n->next = c;
    }
    for (struct RandomNode* n = head; n; n = n->next->next)
        if (n->random) n->next->random = n->random->next;
    struct RandomNode dummy = {0, NULL, NULL}, *tail = &dummy;
    for (struct RandomNode* n = head; n; n = n->next) {
        tail->next = n->next;
        tail = tail->next;
        n->next = tail->next;
    }
    return dummy.next;
}
