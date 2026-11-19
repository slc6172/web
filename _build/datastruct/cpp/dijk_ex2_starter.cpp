#include <iostream>
#include <vector>

const int INF = 1000000000;

// 鬆弛(relax):如果「走到 u 的距離 du + 這條邊的權重 w」比目前記的 dist[v] 更短,
// 就更新 dist[v] 並回傳 true;否則什麼都不改、回傳 false。
bool relax(std::vector<int>& dist, int du, int v, int w) {
    (void)dist;
    (void)du;
    (void)v;
    (void)w;
    return false;
}

int main() {
    std::vector<int> dist = {0, INF, 9};
    std::cout << relax(dist, 0, 1, 7) << " " << dist[1] << " " << relax(dist, 7, 2, 5) << " " << dist[2] << " " << relax(dist, 7, 2, 2) << " " << dist[2] << "\n";   // 預期輸出 1 7 0 9 0 9(最後一次 7+2 = 9,和原本一樣長,不算更短)
}
