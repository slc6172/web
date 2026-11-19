#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Player {
    std::string name;
    int score;
};

int main() {
    std::vector<Player> players = {{"Cara", 80}, {"Ann", 90}, {"Bob", 80}, {"Dan", 90}};
    // 用 std::sort 排:分數高的在前;分數相同時,名字照字母順序(小的在前)。
    // 提示:在 lambda 裡先比分數,分數相同再比名字。
    std::sort(players.begin(), players.end(), [](const Player& a, const Player& b) {
        (void)a;
        (void)b;
        return false;
    });
    for (const Player& p : players) {
        std::cout << p.name << " ";
    }
    std::cout << "\n";                       // 預期輸出 Ann Dan Bob Cara
}
