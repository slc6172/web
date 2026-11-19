#include <iostream>
#include <vector>                           //@ 使用 vector 要先引入 <vector>。
using namespace std;

int main() {
    vector<int> v = {3, 5, 8};              //@ vector<int>:裝 int 的 vector。尖括號裡放元素的型態。
    v.push_back(10);                        //@ push_back:在最後面加一個新元素。vector 會自動變長。
    cout << "長度:" << v.size() << endl;    //@ size():目前有幾個元素。
    cout << "v[1] = " << v[1] << endl;      //@ 取元素的方式和陣列一樣,索引從 0 開始。
    for (int x : v) {
        cout << x << " ";
    }
    cout << endl;
    v.pop_back();                           //@ pop_back:移除最後一個元素。
    cout << "現在長度:" << v.size() << endl;
    return 0;
}
