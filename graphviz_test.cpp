#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void draw_tree() {
    ofstream file("tree.dot");
    file << "digraph {\n"
         << "  A [label=\"AAA\"]\n"
         << "  B [label=\"BBB\"]\n"
         << "  C [label=\"CCC\"]\n"
         << "  D [label=\"DDD\"]\n"
         << "  E [label=\"EEE\"]\n"
         << "  F [label=\"FFF\"]\n"
         << "  G [label=\"GGG\"]\n"
         << "  A -> B\n"
         << "  A -> C\n"
         << "  B -> D\n"
         << "  B -> E\n"
         << "  C -> F\n"
         << "  C -> G\n"
         << "}\n";
    file.close();
    system("dot -Tpng tree.dot -o tree.png");
}

int main() {
    draw_tree();
    return 0;
}