#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;
    v.reserve(100);                      // 一次先要 100 格,之後 push_back 不用再搬家
    for (int i = 0; i < 100; ++i) {
        v.push_back(i);
    }
    std::cout << "size = " << v.size() << ", capacity = " << v.capacity() << "\n";
}
