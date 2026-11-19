#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "要印哪一個數字的乘法表?";
    cin >> n;
    for (int j = 1; j <= 9; j++) {
        cout << n << " x " << j << " = " << n * j << endl;
    }
    return 0;
}
