#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

int countNodes(const TreeNode* node) {
    if (node == nullptr) {
        return 0;
    }
    return 1 + countNodes(node->left) + countNodes(node->right);
}

int main() {
    TreeNode c{3, nullptr, nullptr};
    TreeNode b{2, nullptr, nullptr};
    TreeNode a{1, &b, &c};
    std::cout << countNodes(&a) << " " << countNodes(nullptr) << "\n";
}
