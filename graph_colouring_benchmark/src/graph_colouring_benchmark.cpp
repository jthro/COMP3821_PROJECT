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
#include <random>

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

    for (int num_vertices = 20; num_vertices <= 30; num_vertices += 2) {
        auto cursed = cursed_adjacency_matrix(num_vertices);
        auto normal = random_adjacency_matrix(num_vertices, 10);

        for (int rep = 0; rep < 1000; rep++) {
            std::mt19937 colour_seed{std::random_device{}()};
            std::mt19937 vertex_seed{std::random_device{}()};

            std::vector<colour> initial_colour_normal{
                ColouredGraph::generate_colouring(num_vertices, 10)};
            
            std::vector<colour> initial_colour_cursed{
                ColouredGraph::generate_colouring(num_vertices, 3)};

            ColouredGraph metropolis_cursed{cursed, initial_colour_cursed};
            ColouredGraph middleton_bulseco_cursed{cursed, initial_colour_cursed};

            ColouredGraph metropolis_normal{normal, initial_colour_normal};
            ColouredGraph middleton_bulseco_normal{normal, initial_colour_normal};

            std::println("Naive Metropolis Cursed  | nV = {}, rep = {}", num_vertices, rep);
            NaiveMetropolisRunner(metropolis_cursed, 100, "star", 3, vertex_seed, colour_seed,
                                  writer);

            std::println("Middleton-Bulseco Cursed | nV = {}, rep = {}", num_vertices, rep);
            MiddletonBulsecoRunner(middleton_bulseco_cursed, 100, "star", 3, vertex_seed,
                                   colour_seed, writer);

            std::println("Naive Metropolis Normal  | nV = {}, rep = {}", num_vertices, rep);
            NaiveMetropolisRunner(metropolis_normal, 100, "10-regular", 11, vertex_seed,
                                  colour_seed, writer);

            std::println("Middleton-Bulseco Normal | nV = {}, rep = {}", num_vertices, rep);
            MiddletonBulsecoRunner(middleton_bulseco_normal, 100, "10-regular", 11, vertex_seed,
                                   colour_seed, writer);
        }
    }
}
