#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ofstream first("log.txt");
    first << "第一次執行" << endl;
    first.close();

    ofstream second("log.txt", ios::app);    //@ ios::app:附加模式,從檔案最後面接著寫,不會清空原本的內容。
    second << "第二次執行" << endl;
    second.close();

    ifstream in("log.txt");
    string line;
    while (getline(in, line)) {
        cout << line << endl;
    }
    return 0;
}
