#include <iostream>
#include <queue>
#include <vector>
#include <fstream>
#include <string>
#include <cstring>
using namespace std;

const int N = 3;
const int dx[4] = {-1, 1, 0, 0};
const int dy[4] = {0, 0, -1, 1};

int goal[N][N] = {{1,2,3},{8,0,4},{7,6,5}};

struct Node {
    int state[N][N];
    int f, g, h;
    pair<int, int> zero_pos;
    Node *parent;

    Node(int state[N][N], int g, Node *parent) {
        memcpy(this->state, state, sizeof(this->state));
        this->g = g;
        this->h = calc_h();
        this->f = this->g + this->h;
        this->parent = parent;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (state[i][j] == 0) {
                    zero_pos = {i, j};
                    break;
                }
            }
        }
    }

    int linear_conflict(int state[N][N]) {
    int conflicts = 0;
    for (int i = 0; i < N; i++) {
        int max_col[N] = {0};
        int max_row[N] = {0};
        for (int j = 0; j < N; j++) {
            if (state[i][j] != 0 && (state[i][j] - 1) / N == i) {
                for (int k = 0; k < j; k++) {
                    if (state[i][k] != 0 && (state[i][k] - 1) / N == i && state[i][k] > state[i][j]) {
                        conflicts += 2;
                    }
                }
            }
            if (state[j][i] != 0 && (state[j][i] - 1) % N == i) {
                for (int k = 0; k < j; k++) {
                    if (state[k][i] != 0 && (state[k][i] - 1) % N == i && state[k][i] > state[j][i]) {
                        conflicts += 2;
                    }
                }
            }
        }
    }
    return conflicts;
    }

    int calc_h() {
        int h = 0;
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (state[i][j] != 0) {
                    int goal_i = (state[i][j] - 1) / N;
                    int goal_j = (state[i][j] - 1) % N;
                    h += abs(i - goal_i) + abs(j - goal_j);
                }
            }
        }
        h += linear_conflict(state);
        return h;
    }




    bool is_goal() {
        return h == 0;
    }

    bool operator<(const Node &other) const {
        return f > other.f;
    }
};

void print_state(int state[N][N], ostream &os) {
    os << "[";
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (state[i][j] == 0) os << " ";
            else os << state[i][j];
            if (i != N - 1 || j != N - 1) os << ", ";
        }
    }
    os << "]";
}

void print_path(Node *node) {
    if (node == nullptr) return;
    print_path(node->parent);
}

void print_list(priority_queue<Node*> list, ostream &os) {
    vector<Node*> temp;
    while (!list.empty()) {
        Node *node = list.top();
        list.pop();
        temp.push_back(node);
    }
    for (Node *node : temp) {
        print_state(node->state, os);
        os << "; g=" << node->g << "; h=" << node->h << "; f=" << node->f << endl;
    }
}

void print_list(vector<Node*> list, ostream &os) {
    for (Node *node : list) {
        print_state(node->state, os);
        os << "; g=" << node->g << "; h=" << node->h << "; f=" << node->f << endl;
    }
}

bool is_solvable(int state[N][N]) {
 int inv_count = 0;
 for (int i = 0; i < N * N - 1; i++) {
 for (int j = i + 1; j < N * N; j++) {
 int a = state[i / N][i % N];
 int b = state[j / N][j % N];
 if (a != 0 && b != 0 && a > b) inv_count++;
 }
 }
 cout << "inv_count: " << inv_count << endl;
 return inv_count % 2 == 0;
}



bool is_valid(int x, int y) {
    return x >= 0 && x < N && y >= 0 && y < N;
}

void a_star_search(int initial[N][N], string student_name) {
 if (!is_solvable(initial)) {
 cout << "No solution" << endl;
 return;
 }

 priority_queue<Node*> open_list;
 vector<Node*> closed_list;

 open_list.push(new Node(initial, 0, nullptr));

 ofstream file(student_name + ".txt");
 file << student_name << endl;
 file << "Search A*" << endl;

 file << "Estado Inicial" << endl;
 for (int i = 0; i < N; i++) {
 for (int j = 0; j < N; j++) {
 if (initial[i][j] == 0) file<<" ";
 else file<<initial[i][j];
 if(j!=N-1)file<<", ";
 }
 file<<endl;
 }

 file<<endl;

 file<<"Estado Final"<<endl;

 for (int i = 0; i < N; i++) {
 for (int j = 0; j < N; j++) {
 if(goal[i][j]==0)file<<" ";
 else file<<goal[i][j];
 if(j!=N-1)file<<", ";
 }
 file<<endl;
 }

 int iteration=1;

 while (!open_list.empty()) {

 Node *current_node=open_list.top();
 open_list.pop();
 closed_list.push_back(current_node);

 cout << "current node: ";
 print_state(current_node->state, cout);
 cout << "; g=" << current_node->g << "; h=" << current_node->h << "; f=" << current_node->f << endl;

 file<<"Open:"<<endl;
 print_list(open_list,file);

 file<<"Closed:"<<endl;
 print_list(closed_list,file);

 if(current_node->is_goal()){
 cout<<"Solution found"<<endl;

 file.close();
 return ;
 }

 for(int k=0;k<4;k++){
 int new_x=current_node->zero_pos.first+dx[k];
 int new_y=current_node->zero_pos.second+dy[k];
 if(!is_valid(new_x,new_y))continue;

 int new_state[N][N];
 memcpy(new_state,current_node->state,sizeof(new_state));
 swap(new_state[current_node->zero_pos.first][current_node->zero_pos.second],new_state[new_x][new_y]);

 open_list.push(new Node(new_state,current_node->g+1,current_node));
 }

 file<<endl<<"Iteracion "<<iteration<<endl;

iteration++;
}
file.close();
}



int main() {
 string student_name="Gabriel Pacco Huaraca";
 int initial[N][N]={{2,8,3},{1,6,4},{7,0,5}};

 a_star_search(initial,student_name);
}
