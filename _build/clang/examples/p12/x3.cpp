#include <iostream>
#include <vector>
using namespace std;

void minMax(const vector<int>& v, int& mn, int& mx) {
    mn = v[0];
    mx = v[0];
    for (int x : v) {
        if (x < mn) {
            mn = x;
        }
        if (x > mx) {
            mx = x;
        }
    }
}

int main() {
    vector<int> v = {7, 3, 9, 1, 5};
    int lo, hi;
    minMax(v, lo, hi);
    cout << "最小 " << lo << ",最大 " << hi << endl;
    return 0;
}
