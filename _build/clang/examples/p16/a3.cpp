#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ofstream out("numbers.txt");
    out << "10 20 30 40" << endl;
    out.close();

    ifstream in("numbers.txt");
    int n, sum = 0, count = 0;
    while (in >> n) {                        //@ 和 cin >> 一樣:一個一個讀數字,讀不到時結束。
        sum += n;
        count++;
    }
    cout << "共 " << count << " 個,總和 " << sum << endl;
    return 0;
}
