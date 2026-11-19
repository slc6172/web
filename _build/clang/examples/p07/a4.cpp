#include <iostream>
using namespace std;

int main() {
    int n;
    do {                                 //@ do-while:先做一次,再檢查條件。所以主體「至少會執行一次」。
        cout << "請輸入 1 到 10 的數字:";
        cin >> n;
    } while (n < 1 || n > 10);           //@ 注意 while 的括號後面有分號。條件成立(輸入不合法)就再做一圈。
    cout << "你輸入了 " << n << endl;
    return 0;
}
