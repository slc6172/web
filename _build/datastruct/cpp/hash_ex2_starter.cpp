#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>

// 回傳出現次數最多的單字(假設只有一個最多的)。
// 提示:先用 unordered_map<std::string, int> 數每個單字出現幾次,再找最大的。
std::string mostCommon(const std::vector<std::string>& words) {
    (void)words;
    return "";
}

int main() {
    std::vector<std::string> w = {"cat", "dog", "cat", "bird", "dog", "cat"};
    std::cout << mostCommon(w) << "\n";      // 預期輸出 cat
}
