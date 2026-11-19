#include <iostream>
#include <memory>
using namespace std;

int main() {
    unique_ptr<int> a = make_unique<int>(5);
    unique_ptr<int> b = a;
    cout << *b << endl;
    return 0;
}
