#include <iostream>
using namespace std;

int main() {
    int n = 14;
    cout << "n = " << n << ",是偶數嗎(1 是、0 不是):" << (n % 2 == 0) << endl;
    n = 7;
    cout << "n = " << n << ",是偶數嗎(1 是、0 不是):" << (n % 2 == 0) << endl;
    return 0;
}
