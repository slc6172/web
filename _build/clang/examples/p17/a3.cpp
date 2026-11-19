#include <iostream>
#include <memory>                            //@ 智慧指標在 <memory> 裡。
using namespace std;

int main() {
    unique_ptr<int> p = make_unique<int>(42);    //@ make_unique<int>(42):在 heap 建立一個 int(42),並交給 unique_ptr 管理。
    cout << *p << endl;                      //@ 用法和一般指標一樣:*p 取值。
    *p = 7;
    cout << *p << endl;
    return 0;                                //@ 不需要寫 delete:p 離開範圍時,unique_ptr 會自動歸還。
}
