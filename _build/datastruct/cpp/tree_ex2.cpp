#include <algorithm>
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

int height(const TreeNode* node) {
    if (node == nullptr) {
        return 0;
    }
    return 1 + std::max(height(node->left), height(node->right));
}

int main() {
    TreeNode d{4, nullptr, nullptr};
    TreeNode c{3, &d, nullptr};
    TreeNode b{2, nullptr, nullptr};
    TreeNode a{1, &b, &c};
    std::cout << height(&a) << " " << height(&d) << " " << height(nullptr) << "\n";
}
