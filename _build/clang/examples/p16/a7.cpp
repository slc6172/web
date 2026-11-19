#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ofstream out("data.txt");
    out << "10" << endl << "abc" << endl << "30" << endl;
    out.close();

    ifstream in("data.txt");
    string line;
    int sum = 0, skipped = 0;
    while (getline(in, line)) {
        try {
            sum += stoi(line);               //@ 轉換失敗就丟出例外,直接跳到 catch。
        } catch (const exception& e) {
            skipped++;                       //@ 壞掉的那一行只是被略過,不會讓整個程式停下來。
        }
    }
    cout << "總和 " << sum << ",略過 " << skipped << " 行" << endl;
    return 0;
}
