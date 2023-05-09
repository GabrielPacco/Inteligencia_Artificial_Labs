#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>

using namespace std;

class Node {
public:
    string value;
    Node *left;
    Node *right;
    int level;

    Node(string value, int level) {
        this->value = value;
        this->left = nullptr;
        this->right = nullptr;
        this->level = level;
    }
};

class Tree {
public:
    Node *root;

    Tree() {
        this->root = nullptr;
    }

    void insert(string value) {
        if (this->root == nullptr) {
            this->root = new Node(value, 0);
        } else {
            queue<Node*> q;
            q.push(this->root);

            while (!q.empty()) {
                Node *temp = q.front();
                q.pop();

                if (temp->left != nullptr) {
                    q.push(temp->left);
                } else {
                    temp->left = new Node(value, temp->level + 1);
                    return;
                }

                if (temp->right != nullptr) {
                    q.push(temp->right);
                } else {
                    temp->right = new Node(value, temp->level + 1);
                    return;
                }
            }
        }
    }

    void exportDot() {
        ofstream file("tree.dot");
        file << "digraph g {\n";

        queue<Node*> q;
        q.push(this->root);

        while (!q.empty()) {
            Node *temp = q.front();
            q.pop();

            if (temp->left != nullptr) {
                file << "\"" << temp->value << "\" -> \"" << temp->left->value << "\";\n";
                q.push(temp->left);
            }

            if (temp->right != nullptr) {
                file << "\"" << temp->value << "\" -> \"" << temp->right->value << "\";\n";
                q.push(temp->right);
            }
        }

        file << "}";
        file.close();
    }

    void generateImage() {
        system("dot -Tpng tree.dot -o tree.png");
    }

    bool dfs(Node *node, string goal, vector<pair<string, int>> &frontier, vector<pair<string, int>> &reached) {
        if (node == nullptr) return false;

        frontier.push_back(make_pair(node->value, node->level));
        reached.push_back(make_pair(node->value, node->level));

        ofstream file("dfs.txt", ios::app);

        if (node->value == goal){
            file << "Nodo encontrado -> " << goal << endl;
            return true;
        }

        file << "Paso " << reached.size() << endl;
        file << "frontier = {";
        for (int i = 0; i < frontier.size(); i++) {
            file << frontier[i].first << "(-" << frontier[i].second << ")";
            if (i != frontier.size() - 1) file << ", ";
        }
        file << "}" << endl;
        file << "reached = {";
        for (int i = 0; i < reached.size(); i++) {
            file << reached[i].first << "(-" << reached[i].second << ")";
            if (i != reached.size() - 1) file << ", ";
        }
        file << "}\n";
        file.close();

        if (dfs(node->left, goal, frontier, reached)) return true;
        if (dfs(node->right, goal, frontier, reached)) return true;

        frontier.pop_back();

        return false;
    }
};

int main() {
    Tree tree;

    tree.insert("LAM");
    tree.insert("CUS");
    tree.insert("PUN");
    tree.insert("PIU");
    tree.insert("ANC");
    tree.insert("PAS");
    tree.insert("AMA");
    tree.insert("ICA");
    tree.insert("HUAN");
    tree.insert("MOQ");
    tree.insert("HUA");
    tree.insert("JUN");
    tree.insert("LIM");
    tree.insert("TAC");
    tree.insert("ARE");
    tree.insert("APU");

    tree.exportDot();
    tree.generateImage();

    vector<pair<string, int>> frontier;
    vector<pair<string, int>> reached;
    
    ofstream file("dfs.txt");
    file << "DFS Nodo seleccionado: " << "ARE" << endl;
    file << "Gabriel Pacco Huaraca" << endl;
    file.close();

    bool found = tree.dfs(tree.root, "ARE", frontier, reached);

    cout << "Nodo encontrado: " << (found ? "Si" : "No") << endl;

    return 0;
}