#include <iostream>
#include <cstdlib>
using namespace std;

struct Point {
    int x;
    int y;
};

int manhattan(Point a, Point b) {
    return abs(a.x - b.x) + abs(a.y - b.y);
}

int main() {
    Point p = {1, 2};
    Point q = {4, 6};
    cout << "距離:" << manhattan(p, q) << endl;
    return 0;
}
