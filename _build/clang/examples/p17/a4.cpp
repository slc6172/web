#include <iostream>
#include <memory>
using namespace std;

class Resource {
public:
    Resource() { cout << "取得資源" << endl; }     //@ 建構子:物件被建立時執行。
    ~Resource() { cout << "釋放資源" << endl; }    //@ 解構子(名字前面加 ~):物件被銷毀時自動執行。
};

int main() {
    {                                                //@ 一個內層區塊,用大括號圈出「範圍」。
        unique_ptr<Resource> r = make_unique<Resource>();
        cout << "使用中" << endl;
    }                                                //@ 離開區塊:r 結束生命,unique_ptr 自動讓 Resource 被銷毀,所以印出「釋放資源」。
    cout << "離開區塊之後" << endl;
    return 0;
}
