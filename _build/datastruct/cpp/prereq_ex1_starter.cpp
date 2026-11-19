#include <iostream>

void addOne(int& n) {
    // 在這裡加一行,讓呼叫者的變數加 1
}

int main() {
    int x = 5;
    addOne(x);
    std::cout << x << "\n";                  // 預期輸出 6
}
