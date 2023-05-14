#include <iostream>
#include <queue>
#include <vector>
#include <map>
#include <cmath>
using namespace std;

const int N = 3;
const int N2 = 9;
const int DX[4] = { -1, 0, 1, 0 };
const int DY[4] = { 0, 1, 0, -1 };
const char DIR[4] = { 'u', 'r', 'd', 'l' };

struct Puzzle {
    int f[N2];
    int space;
    int md;
    bool operator < (const Puzzle& p) const {
        for (int i = 0; i < N2; i++) {
            if (f[i] == p.f[i]) continue;
            return f[i] > p.f[i];
        }
        return false;
    }
};

struct State {
    Puzzle puzzle;
    int cost;
    int est;
    bool operator < (const State& s) const {
        return cost + est > s.cost + s.est;
    }
};

int get_md(Puzzle& p) {
    int sum = 0;
    for (int i = 0; i < N2; i++) {
        if (p.f[i] == N2) continue;
        sum += abs(i / N - p.f[i] / N) + abs(i % N - p.f[i] % N % N);
    }
    return sum;
}

bool is_solved(Puzzle& p) {
    for (int i = 0; i < N2; i++) {
        if (p.f[i] != i + 1) return false;
    }
    return true;
}

void print_ans(vector<State>& path) {
    for (int i = 0; i < path.size(); i++) {
        for (int j = 0; j < N2; j++) {
            if (j % N == 0) cout << endl;
            cout << path[i].puzzle.f[j] << " ";
        }
        cout << endl;
        if (i < path.size() - 1) cout << DIR[path[i+1].puzzle.space - path[i].puzzle.space];
    }
    cout << endl;
}

void solve(Puzzle& p) {
    priority_queue<State> q;
    map<Puzzle, int> mp;
    State init;
    init.puzzle = p;
    init.cost = 0;
    init.est = get_md(p);
    q.push(init);
    while (!q.empty()) {
        State s = q.top();
        q.pop();
        Puzzle u = s.puzzle;
        if (mp[u]) continue;
        mp[u] = s.cost;
        if (is_solved(u)) {
            vector<State> path;
            while (s.cost > 0) {
                path.push_back(s);
                s = q.top();
                q.pop();
            }
            path.push_back(s);
            reverse(path.begin(), path.end());
            print_ans(path);
            return;
        }
        for (int r = 0; r < 4; r++) {
            int tx = u.space / N + DX[r];
            int ty = u.space % N + DY[r];
            if (tx < 0 || ty < 0 || tx >= N || ty >= N) continue;
            Puzzle v = u;
            swap(v.f[u.space], v.f[tx * N + ty]);
            v.space = tx * N + ty;
            if (!mp[v]) {
                State ns;
                ns.puzzle = v;
                ns.cost = s.cost + 1;
                ns.est = get_md(v);
                q.push(ns);
            }
        }
    }
}

int main() {
    Puzzle in;
    cout << "Nombre: Gabriel Pacco Huaraca" << endl;
    cout << "Busqueda: A* Search" << endl;
    cout << "Estado inicial: ";
    for (int i = 0; i < N2; i++) {
        cin >> in.f[i];
        if (in.f[i] == 0) {
            in.f[i] = N2;
            in.space = i;
        }
    }
    cout << "Estado final: ";
    for (int i = 0; i < N2; i++) {
        int x;
        cin >> x;
        if (x == 0) x = N2;
        in.md += abs(x - 1) / N + abs(x - 1) % N;
        in.f[i] = x;
    }
    solve(in);
    return 0;
}

