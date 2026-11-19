#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ifstream in("no_such_file.txt");
    if (!in.is_open()) {                     //@ is_open():檔案有沒有成功打開?開不了(不存在、沒權限)就是 false。
        cout << "打不開檔案,請確認檔名與位置" << endl;
        return 1;                            //@ 回傳非 0 的值,表示程式不是正常結束。
    }
    cout << "成功開啟" << endl;
    return 0;
}
