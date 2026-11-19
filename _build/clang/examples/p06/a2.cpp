#include <iostream>
using namespace std;

int main() {
    int score;
    cout << "分數:";
    cin >> score;
    if (score >= 90) {
        cout << "A" << endl;
    } else if (score >= 80) {            //@ else if:前面的條件都不成立,才輪到檢查這一個。
        cout << "B" << endl;
    } else if (score >= 60) {
        cout << "C" << endl;
    } else {                             //@ 最後的 else:以上全都不成立時才會做,可以省略。
        cout << "不及格" << endl;
    }
    return 0;
}
