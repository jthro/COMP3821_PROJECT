// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n
// please note -- everything in this program just ignores the diagonal and everything below as we
// assume an undirected simple graph

#include <fstream>

#include "graph.hpp"
#include "jsonl.hpp"

constexpr int n_trials = 5;

int main() {

    JsonlWriter writer{std::ofstream{"output.jsonl", std::ios::binary}};

    for (double k_coeff = 1; k_coeff < 4; k_coeff += 0.1) {
        for (int n = 10; n <= 100; n += 5) {
            for (int i = 0; i < n_trials; i++) {
                int delta = n / 2;
                colour n_colours = static_cast<colour>(k_coeff * delta);
                ColouredGraph g{random_adjacency_matrix(n, delta), n_colours};
                NaiveMetropolisRunner(g, n * n, delta, n_colours, writer);
            }
        }
    }
}
