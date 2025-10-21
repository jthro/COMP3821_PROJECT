// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n
// please note -- everything in this program just ignores the diagonal and everything below as we
// assume an undirected simple graph

#include <print>
#include <random>
#include <ranges>
#include <vector>

#include "graph.hpp"

constexpr size_t delta = 5;
constexpr colour k = 3 * delta + 1;
constexpr size_t n = 10;

int main() {
    std::random_device rd;
    std::mt19937 vertex_gen{rd()};
    std::mt19937 colour_gen{rd()};

    std::uniform_int_distribution<> colour_dist(0,k-1);
    std::uniform_int_distribution<> vertex_dist(0,n-1);

    ColouredGraph g{random_adjacency_matrix(n, delta), k};
    g.print();
    while (!g.valid_colouring()) {
	size_t u = vertex_dist(vertex_gen);
	colour c = colour_dist(colour_gen);
	NaiveMetropolis(g, k, u, c);
    }
    std::println("Done!");
    g.print();
}
