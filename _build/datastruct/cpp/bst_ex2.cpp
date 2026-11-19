#include <iostream>
#include <vector>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

void toSorted(const TreeNode* node, std::vector<int>& out) {
    if (node == nullptr) {
        return;
    }
    toSorted(node->left, out);
    out.push_back(node->val);
    toSorted(node->right, out);
}

int main() {
    TreeNode n1{1, nullptr, nullptr};
    TreeNode n7{7, nullptr, nullptr};
    TreeNode n3{3, &n1, nullptr};
    TreeNode n5{5, &n3, &n7};
    std::vector<int> out;
    toSorted(&n5, out);
    for (int x : out) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}
