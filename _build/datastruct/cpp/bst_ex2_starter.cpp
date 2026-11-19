#include <iostream>
#include <vector>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
};

// 用「中序走訪」把二元搜尋樹的所有值依序放進 out。BST 的中序結果會是由小到大。
void toSorted(const TreeNode* node, std::vector<int>& out) {
    (void)node;
    (void)out;
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
    std::cout << "\n";                       // 預期輸出 1 3 5 7
}
