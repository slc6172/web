#include <iostream>

// 寫一個 swapInt:交換呼叫者傳進來的兩個 int
void swapInt(int& a, int& b) {
}

int main() {
    int a = 3, b = 7;
    swapInt(a, b);
    std::cout << a << " " << b << "\n";      // 預期輸出 7 3
}
