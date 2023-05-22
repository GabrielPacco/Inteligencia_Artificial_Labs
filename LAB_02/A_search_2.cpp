#include <iostream>
#include <vector>
#include <queue>
#include <fstream>

using namespace std;

struct Node {
    vector<vector<int>> data;
    int level;
    int fval;

    Node(const vector<vector<int>>& data, int level, int fval) : data(data), level(level), fval(fval) {}

    void updateFval(const vector<vector<int>>& goal) {
        fval = level + h(data, goal);
    }

    vector<Node> gen_child() const { // Modificado: Marcar como const
        int x, y;
        for (int i = 0; i < data.size(); i++) {
            for (int j = 0; j < data[i].size(); j++) {
                if (data[i][j] == 0) {
                    x = i;
                    y = j;
                    break;
                }
            }
        }

        vector<vector<int>> val_list = {{x, y - 1}, {x, y + 1}, {x - 1, y}, {x + 1, y}};
        vector<Node> children;
        for (const auto& val : val_list) {
            int x2 = val[0];
            int y2 = val[1];
            if (0 <= x2 && x2 < data.size() && 0 <= y2 && y2 < data.size()) {
                vector<vector<int>> temp_puz = data;
                swap(temp_puz[x][y], temp_puz[x2][y2]);
                children.emplace_back(temp_puz, level + 1, 0);
            }
        }
        return children;
    }

    int h(const vector<vector<int>>& start, const vector<vector<int>>& goal) {
        int temp = 0;
        for (int i = 0; i < start.size(); i++) {
            for (int j = 0; j < start[i].size(); j++) {
                if (start[i][j] != goal[i][j] && start[i][j] != 0) {
                    temp += 1;
                }
            }
        }
        return temp;
    }
};

struct Compare {
    bool operator()(const Node& lhs, const Node& rhs) {
        return lhs.fval > rhs.fval;
    }
};

class Puzzle {
public:
    Puzzle(int size) : n(size), open(), closed() {}

    vector<vector<int>> start() {
        return {{2, 8, 3}, {1, 6, 4}, {7, 0, 5}};
    }

    vector<vector<int>> end() {
        return {{1, 2, 3}, {8, 0, 4}, {7, 6, 5}};
    }

    int f(const Node& start, const vector<vector<int>>& goal) {
        return h(start.data, goal) + start.level;
    }

    int h(const vector<vector<int>>& start, const vector<vector<int>>& goal) {
        int temp = 0;
        for (int i = 0; i < start.size(); i++) {
            for (int j = 0; j < start[i].size(); j++) {
                if (start[i][j] != goal[i][j] && start[i][j] != 0) {
                    temp += 1;
                }
            }
        }
        return temp;
    }

    void show(const vector<vector<int>>& state, ofstream& text) {
        text << "[";
        for (int i = 0; i < state.size(); i++) {
            text << "[";
            for (int j = 0; j < state[i].size(); j++) {
                text << state[i][j];
                if (j < state[i].size() - 1) {
                    text << ", ";
                }
            }
            text << "]";
            if (i < state.size() - 1) {
                text << ", ";
            }
        }
        text << "];";
    }

    void dat(const Node& start, const vector<vector<int>>& goal, ofstream& text) {
        show(start.data, text);
        text << "g=" << start.level << "; h=" << h(start.data, goal) << "; f=" << f(start, goal) << "\n";
    }

    void process() {
        ofstream text("resultado.txt");
        text << "Gabriel Pacco Huaraca\n";
        text << "Search A*\n";
        text << "Estado Incial\n";
        vector<vector<int>> start = this->start();
        show(start, text);
        text << "\n---------------------------------------\n";
        text << "Estado Final\n";
        vector<vector<int>> goal = this->end();
        show(goal, text);
        text << "\n---------------------------------------\n";

        Node initial_node(start, 0, 0);
        initial_node.updateFval(goal);
        int hval = h(initial_node.data, goal);

        text << "Open:\n";
        show(initial_node.data, text);
        text << "g=" << initial_node.level << "; h=" << hval << "; f=" << initial_node.fval << "\nClosed:\n";

        priority_queue<Node, vector<Node>, Compare> open;
        open.push(initial_node);
        int it = 0;
        while (!open.empty()) {
            Node cur = open.top();
            open.pop();
            it++;
            text << "Iteracion " << it << "\n";
            text << "Open:\n";
            for (auto& child : cur.gen_child()) {
                child.updateFval(goal);
                dat(child, goal, text);
                open.push(child);
            }
            text << "Closed:\n";
            dat(cur, goal, text);
            text << "\n---------------------------------------\n";
            if (h(cur.data, goal) == 0) {
                break;
            }
        }

        text.close();

        ofstream dotFile("arbol.dot");
        generateDotFile(initial_node, goal, dotFile);
        dotFile.close();

        // Export the image of the tree using Graphviz
        system("dot -Tpng arbol.dot -o arbol.png");
        cout << "Image exported: arbol.png" << endl;
    }

    void generateDotFile(const Node& node, const vector<vector<int>>& goal, ofstream& dotFile) {
        dotFile << "digraph G {\n";
        generateDotNodes(node, goal, dotFile);
        generateDotEdges(node, dotFile);
        dotFile << "}\n";
    }

    void generateDotNodes(const Node& node, const vector<vector<int>>& goal, ofstream& dotFile) {
    if (node.level < 8) {
        dotFile << "node" << node.level << " [label=\"";
        show(node.data, dotFile);
        dotFile << "\\ng=" << node.level << "; h=" << h(node.data, goal) << "; f=" << f(node, goal) << "\"];\n";
        for (auto& child : node.gen_child()) {
            generateDotNodes(child, goal, dotFile);
            }
        }
    }

    void generateDotEdges(const Node& node, ofstream& dotFile) {
    if (node.level < 4) {
        for (auto& child : node.gen_child()) {
            dotFile << "node" << node.level << " -> node" << child.level << ";\n";
            generateDotEdges(child, dotFile);
            }
        }
    }


private:
    int n;
    priority_queue<Node, vector<Node>, Compare> open;
    vector<Node> closed;
};

int main() {
    Puzzle puz(3);
    puz.process();
    return 0;
}
