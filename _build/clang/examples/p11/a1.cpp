#include <iostream>
using namespace std;

int square(int n) {                         //@ 定義函式:回傳型態 int,名字 square,小括號裡是「參數」(收進來的資料)。
    return n * n;                           //@ return 把結果送回給呼叫它的地方,函式到這裡就結束。
}

int main() {
    cout << square(5) << endl;              //@ 呼叫函式:把 5 交給 square,它算完把 25 送回來,cout 再印出。
    cout << square(12) << endl;
    return 0;
}
