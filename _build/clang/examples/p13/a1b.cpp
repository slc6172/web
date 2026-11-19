#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> stock;
    stock["apple"] = 5;
    cout << stock.count("grape") << endl;    //@ count:這個鍵存在嗎?回傳 1(有)或 0(沒有)。只是查詢,不會改動 map。
    cout << stock["grape"] << endl;          //@ 陷阱:用 [] 讀一個不存在的鍵,會「順手新增」這個鍵,值為 0。
    cout << stock.size() << endl;            //@ 所以現在有 2 筆了!
    return 0;
}
