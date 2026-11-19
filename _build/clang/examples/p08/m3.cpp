#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= i; j++) {       //@ 內層條件改成 j <= i:第 i 列只印 i 個,就變成一個三角形。
            cout << j << "x" << i << "=" << setw(2) << i * j << "  ";
        }
        cout << endl;
    }
    return 0;
}
