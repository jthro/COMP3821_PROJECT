#include <print>

#include "graph.hpp"

int main() {
    AdjacencyMatrix<3> m{
        std::array<bool, 3>{false, true, true},
        std::array<bool, 3>{true, false, true},
        std::array<bool, 3>{true, true, false},
    };

    ColouredGraph<3> g{m, {1, 2, 3}};

    std::println("{},", g.num_edges());
    std::println("{},", g.valid_colouring());
    return 0;
}
