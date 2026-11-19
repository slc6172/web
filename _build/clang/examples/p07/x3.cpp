#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "輸入一個大於 1 的整數:";
    cin >> n;
    bool isPrime = true;
    for (int d = 2; d < n; d++) {
        if (n % d == 0) {
            isPrime = false;
            break;
        }
    }
    cout << n << (isPrime ? " 是質數" : " 不是質數") << endl;
    return 0;
}
