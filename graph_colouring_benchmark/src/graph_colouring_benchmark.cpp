// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n
// please note -- everything in this program just ignores the diagonal and everything below as we
// assume an undirected simple graph

#include <filesystem>
#include <fstream>
#include <ios>
#include <print>
#include <random>

#include "graph.hpp"
#include "jsonl.hpp"

constexpr size_t delta = 5;
constexpr colour k = 3 * delta + 1;
constexpr size_t n = 10;

int main() {

    ColouredGraph g{random_adjacency_matrix(n, delta), k};
    auto tmp = NaiveMetropolisRunner{g, n*n, delta, k};
    std::println("Done!");
}
