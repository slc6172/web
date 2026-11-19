#include <iostream>
#include <string>
using namespace std;

int main() {
    try {                                    //@ try:把「可能出錯」的程式放在這裡面。
        int n = stoi("abc");                 //@ stoi 把文字轉成整數。"abc" 轉不了,會「丟出例外」,程式立刻跳出 try。
        cout << "轉換結果:" << n << endl;    //@ 上面丟出例外,這一行就不會執行。
    } catch (const exception& e) {           //@ catch:接住例外並處理。e.what() 是錯誤的簡短說明。
        cout << "轉換失敗:" << e.what() << endl;
    }
    cout << "程式繼續執行" << endl;
    return 0;
}
