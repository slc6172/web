#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ofstream out("scores.txt");
    out << "5 15 25 35" << endl;
    out.close();

    ifstream in("scores.txt");
    int n, sum = 0, count = 0;
    while (in >> n) {
        sum += n;
        count++;
    }
    cout << "共 " << count << " 個,總和 " << sum << ",平均 " << (double)sum / count << endl;
    return 0;
}
