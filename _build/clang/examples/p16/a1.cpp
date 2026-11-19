#include <iostream>
#include <fstream>                           //@ 檔案輸入輸出要引入 <fstream>。
#include <string>
using namespace std;

int main() {
    ofstream out("notes.txt");               //@ ofstream:輸出檔案串流。括號裡是檔名,不存在就建立,存在就清空重寫。
    out << "Hello" << endl;                  //@ 用法和 cout 一模一樣,只是資料送進檔案而不是螢幕。
    out << "C++ 檔案" << endl;
    out.close();                             //@ 寫完關閉,確保內容真的存進檔案。

    ifstream in("notes.txt");                //@ ifstream:輸入檔案串流,用來讀取。
    string line;
    while (getline(in, line)) {              //@ 一行一行讀,讀到檔案結尾,條件變成假,迴圈結束。
        cout << line << endl;
    }
    return 0;
}
