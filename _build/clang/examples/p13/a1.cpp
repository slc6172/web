#include <iostream>
#include <map>                               //@ 使用 map 要引入 <map>。
#include <string>
using namespace std;

int main() {
    map<string, int> stock;                  //@ map<鍵的型態, 值的型態>:像字典,用「鍵」查「值」。這裡鍵是水果名稱,值是庫存數量。
    stock["apple"] = 5;                      //@ 用 [鍵] 放入或修改一筆。鍵不存在就新增,存在就更新。
    stock["banana"] = 3;
    stock["apple"] += 2;
    cout << "apple 有 " << stock["apple"] << endl;
    cout << "共 " << stock.size() << " 種" << endl;
    for (auto& kv : stock) {                 //@ 走訪 map:每個 kv 是一組鍵值。kv.first 是鍵,kv.second 是值。auto 讓編譯器決定型態,& 避免複製。
        cout << kv.first << ": " << kv.second << endl;
    }
    return 0;
}
