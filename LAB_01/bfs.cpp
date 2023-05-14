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

    Node(string value) {
        this->value = value;
        this->left = nullptr;
        this->right = nullptr;
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
            this->root = new Node(value);
        } else {
            queue<Node*> q;
            q.push(this->root);

            while (!q.empty()) {
                Node *temp = q.front();
                q.pop();

                if (temp->left != nullptr) {
                    q.push(temp->left);
                } else {
                    temp->left = new Node(value);
                    return;
                }

                if (temp->right != nullptr) {
                    q.push(temp->right);
                } else {
                    temp->right = new Node(value);
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

    bool bfs(string goal) {
        vector<string> frontier;
        vector<string> reached;

        queue<Node*> q;
        q.push(this->root);

        int step = 1;
        ofstream file("bfs.txt", ios::app);
        file << "BFS Nodo seleccionado: " << goal << endl;
        file << "Gabriel Pacco Huaraca" << endl;
        file.close();
        while (!q.empty()) {
            int size = q.size();

            for (int i = 0; i < size; i++) {
                Node *temp = q.front();
                q.pop();

                frontier.push_back(temp->value);
                reached.push_back(temp->value);

                ofstream file("bfs.txt", ios::app);
                if (temp->value == goal){
                    file << "Nodo encontrado -> " << goal << endl;
                    return true;
                } 
                
                file << "Paso " << step++ << endl;
                file << "frontier = {";
                for (int i = 0; i < frontier.size(); i++) {
                    file << frontier[i];
                    if (i != frontier.size() - 1) file << ", ";
                }
                file << "}" << endl;
                file << "reached = {";
                for (int i = 0; i < reached.size(); i++) {
                    file << reached[i];
                    if (i != reached.size() - 1) file << ", ";
                }
                file << "}\n";
                file.close();

                if (temp->left != nullptr) {
                    q.push(temp->left);
                }

                if (temp->right != nullptr) {
                    q.push(temp->right);
                }
            }
            frontier.clear();
        }
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

    ofstream file("bfs.txt");
    file.close();

    bool found = tree.bfs("ARE");

    cout << "Nodo encontrado: " << (found ? "Si" : "No") << endl;

    return 0;
}