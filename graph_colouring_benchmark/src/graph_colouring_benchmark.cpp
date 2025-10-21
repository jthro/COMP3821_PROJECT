// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n
// please note -- everything in this program just ignores the diagonal and everything below as we
// assume an undirected simple graph

#include <print>
#include <vector>

#include "graph.hpp"

int main() {
    std::vector<colour> cols{};
    ColouredGraph g{random_adjacency_matrix(10, 4), cols};
    g.print();
}
