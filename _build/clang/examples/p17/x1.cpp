#include <iostream>
#include <memory>
using namespace std;

class Resource {
public:
    Resource() { cout << "取得資源" << endl; }
    ~Resource() { cout << "釋放資源" << endl; }
};

void work(bool fail) {
    unique_ptr<Resource> r = make_unique<Resource>();
    if (fail) {
        cout << "發生問題,提早離開" << endl;
        return;
    }
    cout << "正常完成" << endl;
}

int main() {
    work(true);
    work(false);
    return 0;
}
