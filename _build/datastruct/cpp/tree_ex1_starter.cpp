#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

// 回傳這棵樹有幾個節點。空的樹(nullptr)是 0 個。
// 提示:節點數 = 1(自己)+ 左子樹節點數 + 右子樹節點數
int countNodes(const TreeNode* node) {
    (void)node;
    return 0;
}

int main() {
    TreeNode c{3, nullptr, nullptr};
    TreeNode b{2, nullptr, nullptr};
    TreeNode a{1, &b, &c};
    std::cout << countNodes(&a) << " " << countNodes(nullptr) << "\n";   // 預期輸出 3 0
}
