#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {3, 1, 3, 2, 1, 4};
    vector<int> result;
    for (int x : v) {
        bool found = false;
        for (int u : result) {
            if (u == x) {
                found = true;
                break;
            }
        }
        if (!found) {
            result.push_back(x);
        }
    }
    for (int u : result) {
        cout << u << " ";
    }
    cout << endl;
    return 0;
}
