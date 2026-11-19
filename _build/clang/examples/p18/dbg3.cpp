#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {80, 92, 75, 60, 88};
    int n = v.size();
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += v[i];
    }
    cout << "平均:" << sum / (double)n << endl;
    return 0;
}
