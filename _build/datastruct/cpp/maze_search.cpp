#include <iostream>
#include <queue>
#include <stack>
#include <string>
#include <vector>

struct Point {
    int r;
    int c;
};

struct Step {
    Point p;
    int steps;
};

const int DR[4] = {-1, 1, 0, 0};
const int DC[4] = {0, 0, -1, 1};

bool isOpen(const std::vector<std::string>& g, int r, int c) {
    return r >= 0 && r < static_cast<int>(g.size()) && c >= 0 && c < static_cast<int>(g[0].size()) && g[r][c] != '#';
}

int bfs(const std::vector<std::string>& g, Point s, Point t) {
    std::vector<std::vector<int>> dist(g.size(), std::vector<int>(g[0].size(), -1));
    std::queue<Point> q;
    dist[s.r][s.c] = 0;
    q.push(s);
    while (!q.empty()) {
        Point cur = q.front();
        q.pop();
        if (cur.r == t.r && cur.c == t.c) {
            return dist[cur.r][cur.c];
        }
        for (int d = 0; d < 4; ++d) {
            int nr = cur.r + DR[d];
            int nc = cur.c + DC[d];
            if (isOpen(g, nr, nc) && dist[nr][nc] == -1) {
                dist[nr][nc] = dist[cur.r][cur.c] + 1;
                q.push({nr, nc});
            }
        }
    }
    return -1;
}

int dfs(const std::vector<std::string>& g, Point s, Point t) {
    std::vector<std::vector<bool>> seen(g.size(), std::vector<bool>(g[0].size(), false));
    std::stack<Step> st;
    st.push({s, 0});
    while (!st.empty()) {
        Step cur = st.top();
        st.pop();
        if (seen[cur.p.r][cur.p.c]) {
            continue;
        }
        seen[cur.p.r][cur.p.c] = true;
        if (cur.p.r == t.r && cur.p.c == t.c) {
            return cur.steps;
        }
        for (int d = 0; d < 4; ++d) {
            int nr = cur.p.r + DR[d];
            int nc = cur.p.c + DC[d];
            if (isOpen(g, nr, nc) && !seen[nr][nc]) {
                st.push({{nr, nc}, cur.steps + 1});
            }
        }
    }
    return -1;
}

int main() {
    std::vector<std::vector<std::string>> mazes = {
        {"S......", ".......", ".......", ".......", "......G"},
        {"S....##", ".##....", ".#.....", "#..##..", "......G"},
        {"S.#....", ".#.###.", ".#...#.", ".###.#.", "....#.G"},
    };
    for (const auto& g : mazes) {
        Point s{0, 0};
        Point t{static_cast<int>(g.size()) - 1, static_cast<int>(g[0].size()) - 1};
        std::cout << "BFS 最短步數 " << bfs(g, s, t) << ",DFS 走到的步數 " << dfs(g, s, t) << "\n";
    }
}
