#pragma once

#include <algorithm>
#include <iterator>
#include <numeric>
#include <optional>
#include <print>
#include <random>
#include <ranges>
#include <tuple>
#include <vector>

using colour = long long;

struct ColourSuccess {};

// Generate a sequence of integer pairs corresponding to upper triangular (minus the diagonal)
// indices of a square matrix
inline auto upper_triangular_range(size_t n) {
    return std::views::cartesian_product(std::ranges::iota_view{0uz, n},
                                         std::ranges::iota_view{0uz, n}) |
           std::views::filter([](std::tuple<size_t, size_t> pair) {
               return std::get<1>(pair) > std::get<0>(pair);
           });
}

struct AdjacencyMatrix : std::vector<std::vector<bool>> {
    auto compute_num_edges() const -> int {
        // Read as:
        // Take a sequence of ints corresponding to upper triangular (minus the diagonal indices) ->
        // transform them into 1 if connected, 0 otherwise -> sum
        auto r = upper_triangular_range(size()) |
                 std::views::transform([this](std::tuple<size_t, size_t> pair) {
                     return static_cast<int>((*this)[std::get<0>(pair)][std::get<1>(pair)]);
                 });
        return std::accumulate(r.begin(), r.end(), 0);
    }
};

// https://arxiv.org/pdf/1509.06985
// much simplified as \Delta \in \{k\}, k \in \mathbb{N}, not a distribution
inline auto random_adjacency_matrix(size_t n_v, size_t degree) -> AdjacencyMatrix {
    std::vector<std::vector<bool>> matrix(n_v, std::vector<bool>(n_v, false));

    std::vector<size_t> stubs{};
    for (size_t i : std::views::iota(0uz, n_v)) {
        for (size_t j : std::views::iota(0uz, degree)) stubs.emplace_back(i);
    }

    std::vector<size_t> order{};
    std::shuffle(stubs.begin(), stubs.end(), std::mt19937{std::random_device{}()});
    for (auto pair : stubs | std::views::slide(2)) {
        const size_t u = pair[0];
        const size_t v = pair[1];
        matrix[u][v] = true;
        matrix[v][u] = true;
    }

    return AdjacencyMatrix{matrix};
}

class ColouredGraph {
   private:
    AdjacencyMatrix m_matrix{};
    std::vector<colour> m_colouring{};
    const int m_num_edges;

   public:
    template <typename T>
    explicit ColouredGraph(T&& matrix, std::vector<colour> colouring)
        : m_matrix{std::forward<T>(matrix)},
          m_colouring{std::move(colouring)},
          m_num_edges{m_matrix.compute_num_edges()} {}

    auto get_colouring() const -> const std::vector<colour>& { return m_colouring; }

    // Returns std::nullopt if the colouring failed
    // Returns marker struct if the colouring succeeded
    // Note: this does not necessarily imply the whole colouring is valid
    auto recolour(int vertex, colour colour) -> std::optional<ColourSuccess> {
        for (int neighbour : std::ranges::iota_view{0uz, m_matrix.size()}) {
            bool connected = m_matrix[vertex][neighbour];
            int neighbour_colour = m_colouring[neighbour];
            if (connected && colour == neighbour_colour) return std::nullopt;
        }

        m_colouring[vertex] = colour;
        return ColourSuccess{};
    }

    auto num_vertices() const -> int { return m_matrix.size(); }

    auto num_edges() const -> const int& { return m_num_edges; }

    auto valid_colouring() -> bool {
        auto r = upper_triangular_range(m_matrix.size()) |
                 std::views::transform([this](std::tuple<size_t, size_t> pair) {
                     return (!(m_matrix[std::get<0>(pair)][std::get<1>(pair)] &&
                               m_colouring[std::get<0>(pair)] == m_colouring[std::get<1>(pair)]));
                 });
        // (fold && r true)
        return std::accumulate(r.begin(), r.end(), true, [](bool a, bool b) { return a && b; });
    }

    void print() const {
        std::println("{}", m_matrix);
        std::println("Colours: {}", m_colouring);
    }
};
