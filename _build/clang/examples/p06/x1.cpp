#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "整數:";
    cin >> n;
    if (n % 2 == 0) {
        cout << n << " 是偶數" << endl;
    } else {
        cout << n << " 是奇數" << endl;
    }
    return 0;
}
