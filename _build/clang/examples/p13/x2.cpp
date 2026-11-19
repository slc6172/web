#include <iostream>
#include <vector>
#include <set>
using namespace std;

int main() {
    vector<int> v = {5, 3, 5, 1, 3, 9};
    set<int> s;
    for (int x : v) {
        s.insert(x);
    }
    for (int x : s) {
        cout << x << " ";
    }
    cout << endl;
    return 0;
}
