#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Player {
    std::string name;
    int score;
};

int main() {
    std::vector<Player> players = {{"A", 90}, {"B", 85}, {"C", 90}, {"D", 85}};
    std::stable_sort(players.begin(), players.end(),
                     [](const Player& a, const Player& b) { return a.score > b.score; });
    for (const Player& p : players) {
        std::cout << p.name << ":" << p.score << " ";
    }
    std::cout << "\n";
}
