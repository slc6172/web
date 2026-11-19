#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ofstream out("names.txt");
    out << "Mina" << endl << "Leo" << endl << "Amy" << endl;
    out.close();

    ifstream in("names.txt");
    string line;
    int no = 1;
    while (getline(in, line)) {
        cout << no << ". " << line << endl;
        no++;
    }
    return 0;
}
