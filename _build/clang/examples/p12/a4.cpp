#include <iostream>
#include <string>
using namespace std;

void printInfo(const string& s) {            //@ const 參考:不複製、只是「借來看」,而且保證不會改到它。傳大的資料(字串、vector)時很常用。
    cout << s << "(" << s.length() << " 個字元)" << endl;
}

int main() {
    string name = "Mina Chen";
    printInfo(name);
    return 0;
}
