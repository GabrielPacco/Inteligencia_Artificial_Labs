#include <iostream>
#include <queue>
#include <vector>

using namespace std;

/*BFS en c++ tomando un arcbol de caracteres*/
/*Encontrar el elemento que se desea*/
void bfs(vector<char> adj[], int n, char start) {
    bool visited[n] = {false};
    queue<char> q;
    visited[start] = true;
    q.push(start);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        cout << u << " ";
        for (int v : adj[u]) {
            if (!visited[v]) {
                visited[v] = true;
                q.push(v);
            }
        }
    }
}

int main() {
    int n;
    char search;

    n = 17;
    vector<char> adj[n];
    
    adj[0].push_back('TAC');
    adj[1].push_back('PUN');
    adj[2].push_back('PIU');
    adj[3].push_back('CUS');
    adj[4].push_back('LAM');
    adj[5].push_back('PAS');
    adj[6].push_back('ICA');
    adj[7].push_back('HUAN');
    adj[8].push_back('MOQ');
    adj[9].push_back('HUA');
    adj[10].push_back('JUN');
    adj[11].push_back('CAL');
    adj[12].push_back('AYA');
    adj[13].push_back('ANC');
    adj[14].push_back('AMA');
    adj[15].push_back('ARE');
    adj[16].push_back('APU');


    char start;
    start = 'TAC';
    bfs(adj, n, start);
    return 0;
}