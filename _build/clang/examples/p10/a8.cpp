#include <iostream>
#include <cstring>                           //@ strlen 在 <cstring> 裡。
using namespace std;

int main() {
    char word[] = "Hi!";                     //@ C 風格字串:一個 char 陣列,結尾自動放一個看不見的 '\0' 作為「結束記號」。
    cout << word << endl;
    cout << strlen(word) << endl;            //@ strlen 算出文字有幾個字元(不含結束記號):3。
    cout << sizeof(word) << endl;            //@ sizeof 算出陣列佔幾格:'H'、'i'、'!' 加上 '\0',共 4。
    return 0;
}
