#include <iostream>
#include <string>
#include <vector>

using Table = std::vector<std::vector<std::string>>;

int hashOf(const std::string& key, int m) {
    int sum = 0;
    for (char c : key) {
        sum += c;
    }
    return sum % m;
}

bool contains(const Table& t, const std::string& key) {
    int idx = hashOf(key, static_cast<int>(t.size()));
    for (const std::string& k : t[idx]) {
        if (k == key) {
            return true;
        }
    }
    return false;
}

void insert(Table& t, const std::string& key) {
    if (contains(t, key)) {
        return;
    }
    int idx = hashOf(key, static_cast<int>(t.size()));
    t[idx].push_back(key);
}

void erase(Table& t, const std::string& key) {
    int idx = hashOf(key, static_cast<int>(t.size()));
    std::vector<std::string>& bucket = t[idx];
    for (int i = 0; i < static_cast<int>(bucket.size()); ++i) {
        if (bucket[i] == key) {
            bucket.erase(bucket.begin() + i);
            return;
        }
    }
}

void print(const Table& t) {
    for (int i = 0; i < static_cast<int>(t.size()); ++i) {
        std::cout << i << ":";
        for (const std::string& k : t[i]) {
            std::cout << " " << k;
        }
        std::cout << "\n";
    }
}

int main() {
    Table t(7);                              // 7 個桶子
    for (const char* w : {"cat", "act", "dog", "god", "bird"}) {
        insert(t, w);
    }
    print(t);
    std::cout << contains(t, "act") << contains(t, "tac") << "\n";
    erase(t, "cat");
    std::cout << contains(t, "cat") << contains(t, "act") << "\n";
}
