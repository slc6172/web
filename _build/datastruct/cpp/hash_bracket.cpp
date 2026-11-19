#include <iostream>
#include <string>
#include <unordered_map>

int main() {
    std::unordered_map<std::string, int> m;
    std::cout << "size before = " << m.size() << "\n";
    if (m["x"] == 0) {                       // 只是想「看看有沒有」,卻不小心新增了 x
        std::cout << "x is zero\n";
    }
    std::cout << "size after = " << m.size() << "\n";
    std::cout << "count(y) = " << m.count("y") << ", size = " << m.size() << "\n";   // count 不會新增
}
