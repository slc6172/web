#include <iostream>
using namespace std;

int main() {
    int n, sum = 0;
    cout << "輸入數字(輸入 0 結束):";
    cin >> n;
    while (n != 0) {                     //@ while:每圈開始前先檢查條件,成立才進去。次數事先不知道時很好用。
        sum += n;
        cin >> n;                        //@ 迴圈裡一定要有改變條件的動作(這裡是讀下一個數字),否則會一直轉下去。
    }
    cout << "總和:" << sum << endl;
    return 0;
}
