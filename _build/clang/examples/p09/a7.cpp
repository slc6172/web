#include <iostream>
using namespace std;

int main() {
    int grid[2][3] = {{1, 2, 3}, {4, 5, 6}};   //@ 二維陣列:2 列、3 欄。想成一張表格,用 grid[列][欄] 取值。
    for (int r = 0; r < 2; r++) {
        for (int c = 0; c < 3; c++) {
            cout << grid[r][c] << " ";
        }
        cout << endl;
    }
    cout << grid[1][2] << endl;                //@ 第 2 列(索引 1)第 3 欄(索引 2):6。
    return 0;
}
