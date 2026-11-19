#include <algorithm>
#include <iostream>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

// 回傳樹的高度:最長的那條路徑上有幾個節點。空的樹是 0,只有一個節點是 1。
// 提示:高度 = 1 + max(左子樹高度, 右子樹高度)
int height(const TreeNode* node) {
    (void)node;
    return 0;
}

int main() {
    TreeNode d{4, nullptr, nullptr};
    TreeNode c{3, &d, nullptr};
    TreeNode b{2, nullptr, nullptr};
    TreeNode a{1, &b, &c};
    std::cout << height(&a) << " " << height(&d) << " " << height(nullptr) << "\n";   // 預期輸出 3 1 0
}
