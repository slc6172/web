#include <iostream>
using namespace std;

int main() {
    int n, count = 0, maxValue = 0;
    cout << "輸入正整數(輸入 0 結束):";
    cin >> n;
    while (n != 0) {
        count++;
        if (n > maxValue) {
            maxValue = n;
        }
        cin >> n;
    }
    cout << "共 " << count << " 個數字,最大的是 " << maxValue << endl;
    return 0;
}
