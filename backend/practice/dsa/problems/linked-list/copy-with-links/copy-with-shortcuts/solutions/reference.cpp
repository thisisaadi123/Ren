class Solution {
public:
    RandomNode* copyList(RandomNode* head) {
        unordered_map<RandomNode*, RandomNode*> copy;
        copy[nullptr] = nullptr;
        for (RandomNode* n = head; n; n = n->next) copy[n] = new RandomNode(n->val);
        for (RandomNode* n = head; n; n = n->next) {
            copy[n]->next = copy[n->next];
            copy[n]->random = copy[n->random];
        }
        return copy[head];
    }
};
