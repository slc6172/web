#include <iostream>
#include <set>                               //@ 使用 set 要引入 <set>。
using namespace std;

int main() {
    set<int> s = {3, 1, 2, 3, 1};            //@ set:不會重複的集合。放進相同的值,只會留一份;而且會自動由小到大排好。
    for (int x : s) {
        cout << x << " ";
    }
    cout << endl;
    s.insert(5);                             //@ insert:加入一個元素。
    s.erase(1);                              //@ erase:移除一個元素。
    cout << "有 2 嗎?" << s.count(2) << endl;    //@ count:有就是 1,沒有就是 0。
    cout << "共 " << s.size() << " 個" << endl;
    return 0;
}
