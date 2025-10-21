// Graph colouring algorithm benchmark
// Test format:
// - 5 different n to accurately see limiting time complexity
// - Range Delta from 2 to n
// - Range k from Delta + true to n

#include <print>
#include <vector>

#include "graph.hpp"

int main() {
    ColouredGraph g{std::vector<std::vector<bool>>{{false,true,true},{true,false,true},{true,true,false}}, {1,2,2}};
    std::println("{}", g.valid_colouring());
}
