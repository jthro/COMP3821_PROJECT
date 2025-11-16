// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n
// please note -- everything in this program just ignores the diagonal and everything below as we
// assume an undirected simple graph

#include <cmath>
#include <fstream>
#include <print>

#include "graph.hpp"
#include "jsonl.hpp"

int main() {
    JsonlWriter writer{std::ofstream{"output.jsonl", std::ios::binary}};

    // for (double k_coeff = 1; k_coeff < 4; k_coeff += 0.1) {
    //     for (int n = 10; n <= 100; n += 5) {
    //         for (int i = 0; i < s; i++) {
    //             int delta = n / 2;
    //             colour n_colours = static_cast<colour>(k_coeff * delta);
    //             ColouredGraph g{random_adjacency_matrix(n, delta), n_colours};
    //             NaiveMetropolisRunner(g, n * n, delta, n_colours, writer);
    //         }
    //     }
    // }

    for (int num_vertices = 5; num_vertices <= 100; num_vertices += 5) {
        for (int k = 10; k <= 14; k += 1) {
            for (int rep = 0; rep < 10; rep++) {
                ColouredGraph g{random_adjacency_matrix(num_vertices, 10), k};

		std::println("Naive Metropolis  | nV = {}, k = {}", num_vertices, k);
                NaiveMetropolisRunner(g, std::pow(num_vertices, 2), 10, k, writer);
		std::println("Middleton-Bulseco | nV = {}, k = {}", num_vertices, k);                
                MiddletonBulsecoRunner(g, std::pow(num_vertices, 2), 10, k, writer);
		std::println("Flip Dynamics | nV = {}, k = {}", num_vertices, k);
		FlipDynamicsRunner(g, std::pow(num_vertices, 2), 10, k, writer);
            }
        }
    }
    
    // for (int num_vertices = 20; num_vertices <= 30; num_vertices += 2) {
    //     for (int k = 10; k <= 30; k += 10) {
    //         for (int rep = 0; rep < 1000; rep++) {
    //             AdjacencyMatrix m{random_adjacency_matrix(num_vertices, 10)};
    //             std::vector<colour> initial_colour{
    //                 ColouredGraph::generate_colouring(num_vertices, k)};
    //             ColouredGraph metropolis{m, initial_colour};
    //             ColouredGraph middleton_bulseco{m, initial_colour};

    //             std::println("Naive Metropolis  | nV = {}, k = {}", num_vertices, k);
    //             NaiveMetropolisRunner(metropolis, std::pow(num_vertices, 2), 10, k, writer);
    //             std::println("Middleton-Bulseco | nV = {}, k = {}", num_vertices, k);
    //             MiddletonBulsecoRunner(middleton_bulseco, std::pow(num_vertices, 2), 10, k, writer);
    //         }
    //     }
    // }
}
