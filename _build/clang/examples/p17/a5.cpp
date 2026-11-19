#include <iostream>
using namespace std;

class Resource {
public:
    Resource() { cout << "取得資源" << endl; }
    ~Resource() { cout << "釋放資源" << endl; }
    void use() { cout << "使用中" << endl; }
};

int main() {
    {
        Resource* r = new Resource();        //@ 用原始的 new:要自己負責 delete。
        r->use();
    }                                        //@ 忘了 delete r;!r 這個指標消失了,heap 上的物件卻還在,沒有人能再歸還它。
    cout << "離開區塊之後" << endl;
    return 0;
}
