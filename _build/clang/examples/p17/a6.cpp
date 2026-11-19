#include <iostream>
#include <memory>
using namespace std;

int main() {
    shared_ptr<int> a = make_shared<int>(10);    //@ shared_ptr:可以有好幾個擁有者,最後一個離開時才歸還。
    cout << a.use_count() << endl;           //@ use_count():目前有幾個擁有者。
    shared_ptr<int> b = a;                   //@ 複製 shared_ptr:現在 a 與 b 共同擁有同一個 int。
    cout << a.use_count() << endl;
    b.reset();                               //@ b 放手,擁有者少一個。
    cout << a.use_count() << endl;
    return 0;
}
