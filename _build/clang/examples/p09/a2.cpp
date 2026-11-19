#include <iostream>
using namespace std;

int main() {
    int scores[5] = {80, 92, 75, 60, 88};
    int sum = 0;
    for (int i = 0; i < 5; i++) {           //@ 走訪陣列的標準寫法:i 從 0 開始、小於長度。索引 i 剛好跑過每一個元素。
        sum += scores[i];
    }
    double avg = sum / 5.0;
    cout << "總分:" << sum << endl;
    cout << "平均:" << avg << endl;
    return 0;
}
