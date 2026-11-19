#include <iostream>
#include <memory>
using namespace std;

int main() {
    shared_ptr<int> a = make_shared<int>(5);
    cout << "a 建立後:" << a.use_count() << endl;
    shared_ptr<int> b = a;
    shared_ptr<int> c = a;
    cout << "複製兩次後:" << a.use_count() << endl;
    b.reset();
    cout << "b 放手後:" << a.use_count() << endl;
    return 0;
}
