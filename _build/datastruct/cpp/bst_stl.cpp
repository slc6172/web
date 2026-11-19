#include <iostream>
#include <map>
#include <set>
#include <string>

int main() {
    std::set<int> s = {5, 3, 8, 1};          // 自動平衡的搜尋樹(紅黑樹),元素永遠排好序
    s.insert(4);
    s.erase(3);
    for (int x : s) {
        std::cout << x << " ";               // 由小到大
    }
    std::cout << "\n";
    std::cout << s.count(4) << s.count(3) << "\n";
    auto it = s.lower_bound(5);              // 第一個 >= 5 的元素
    std::cout << *it << "\n";

    std::map<std::string, int> age = {{"Cara", 30}, {"Ann", 25}, {"Bob", 28}};
    for (const auto& entry : age) {
        std::cout << entry.first << "=" << entry.second << " ";   // 依 key 排序
    }
    std::cout << "\n";
}
