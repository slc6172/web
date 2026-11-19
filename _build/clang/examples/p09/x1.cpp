#include <iostream>
using namespace std;

int main() {
    int a[6] = {12, 7, 30, 4, 19, 8};
    int sum = 0, best = a[0];
    for (int i = 0; i < 6; i++) {
        sum += a[i];
        if (a[i] > best) {
            best = a[i];
        }
    }
    cout << "總和:" << sum << endl;
    cout << "平均:" << sum / 6.0 << endl;
    cout << "最大:" << best << endl;
    return 0;
}
