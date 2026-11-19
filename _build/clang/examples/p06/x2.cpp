#include <iostream>
using namespace std;

int main() {
    int score;
    cout << "分數:";
    cin >> score;
    if (score > 100 || score < 0) {
        cout << "分數必須在 0 到 100 之間" << endl;
    } else if (score >= 90) {
        cout << "等級 A" << endl;
    } else if (score >= 70) {
        cout << "等級 B" << endl;
    } else if (score >= 60) {
        cout << "等級 C" << endl;
    } else {
        cout << "等級 D" << endl;
    }
    return 0;
}
