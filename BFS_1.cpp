#include <iostream>
#include <vector>

using namespace std;

struct Node {
    string value;
    vector<Node*> children;
};

void printTree(Node* node, int depth) {
    for (int i = 0; i < depth; i++) {
        cout << "  ";
    }
    cout << node->value << endl;
    for (Node* child : node->children) {
        printTree(child, depth + 1);
    }
}

int main() {
    Node* root = new Node{"abc", {}};
    Node* child1 = new Node{"def", {}};
    Node* child2 = new Node{"ghi", {}};
    Node* grandchild1 = new Node{"jkl", {}};
    Node* grandchild2 = new Node{"mno", {}};
    Node* grandchild3 = new Node{"pqr", {}};
    root->children.push_back(child1);
    root->children.push_back(child2);
    child1->children.push_back(grandchild1);
    child1->children.push_back(grandchild2);
    child2->children.push_back(grandchild3);
    printTree(root, 0);
    return 0;
}