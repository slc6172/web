#include <iostream>
using namespace std;

int main() {
    cout << 2 + 3 * 4 << endl;          //@ 先乘除、後加減,和數學一樣:先算 3 * 4。
    cout << (2 + 3) * 4 << endl;        //@ 括號最優先:先算 2 + 3。
    cout << 10 - 2 - 3 << endl;         //@ 同一層的運算由左往右:(10 - 2) - 3。
    return 0;
}
