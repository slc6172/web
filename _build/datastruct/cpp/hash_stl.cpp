#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::vector<std::string> words = {"cat", "dog", "cat", "bird", "dog", "cat"};
    std::unordered_map<std::string, int> count;
    for (const std::string& w : words) {
        ++count[w];                          // 沒有這個 key 時,會自動建立並從 0 開始
    }
    std::cout << "cat = " << count["cat"] << "\n";
    std::cout << "dog = " << count["dog"] << "\n";
    auto it = count.find("fish");            // 查詢用 find,不會新增
    std::cout << "fish found? " << (it != count.end()) << "\n";
    std::cout << "size = " << count.size() << "\n";
    count.erase("dog");
    std::cout << "has dog? " << count.count("dog") << "\n";
}
