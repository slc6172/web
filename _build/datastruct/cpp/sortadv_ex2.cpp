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
    std::sort(players.begin(), players.end(), [](const Player& a, const Player& b) {
        if (a.score != b.score) {
            return a.score > b.score;
        }
        return a.name < b.name;
    });
    for (const Player& p : players) {
        std::cout << p.name << " ";
    }
    std::cout << "\n";
}
