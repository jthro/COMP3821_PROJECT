// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n
// please note -- everything in this program just ignores the diagonal and everything below as we
// assume an undirected simple graph

#include <cmath>
#include <fstream>

#include "graph.hpp"
#include "jsonl.hpp"
#include "test_parser.hpp"

constexpr size_t delta = 5;
constexpr colour k = 3 * delta + 1;
constexpr size_t n = 10;

int main() {
    // ColouredGraph g{random_adjacency_matrix(n, delta), k};
    // auto tmp = NaiveMetropolisRunner{g, n*n, delta, k};
    // std::println("Done!");

    /// test format:
    /// n: start stop step
    /// delta: start step stop
    /// k: coeff_start, c_start, coeff_stop, c_stop, coeff_step, c_step
    /// trials: number

    TestData config{std::ifstream("input.txt")};
    JsonlWriter writer{std::ofstream{"output.jsonl", std::ios::binary}};

    for (size_t k_coeff = config.delta_coeff_start; k_coeff <= config.delta_coeff_stop;
         k_coeff += config.delta_coeff_stop) {
        for (size_t k_c = config.delta_constant_start; k_c <= config.delta_constant_stop;
             k_c += config.delta_constant_stop) {
	    for (size_t delta = config.delta_start; delta <= config.delta_stop; delta += config.delta_step) {
                for (size_t n = config.n_start; n <= config.n_stop; n += config.n_step) {

                    size_t delta_abs = std::floor(n * delta);

		    for (size_t i : std::ranges::iota_view{0uz, config.n_trials_per}) {
			colour k = k_coeff * delta_abs + k_c;
			ColouredGraph g{random_adjacency_matrix(n, delta_abs), k};
			NaiveMetropolisRunner{g, n*n, delta_abs, k, writer};
                    }
		}
            }
        }
    }
}
