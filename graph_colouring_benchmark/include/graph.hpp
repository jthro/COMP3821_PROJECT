
#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <numeric>
#include <print>
#include <random>
#include <ranges>
#include <tuple>
#include <vector>

#include "jsonl.hpp"

using colour = long long;

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
// assign \Delta stubs to each vertex, sample pairs without replacement, remove self-loops
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

    template <typename T>
    explicit ColouredGraph(T&& matrix, colour n_colours)
        : m_matrix{std::forward<T>(matrix)}, m_num_edges{m_matrix.compute_num_edges()} {
        std::random_device rd;
        std::mt19937 gen{rd()};
        std::uniform_int_distribution<> colour_distribution(0, n_colours - 1);
        for (auto i : std::ranges::iota_view{0uz, m_matrix.size()}) {
            m_colouring.emplace_back(colour_distribution(gen));
        }
    }

    auto get_colouring() const -> const std::vector<colour>& { return m_colouring; }

    auto get_adjacency() const -> const std::vector<std::vector<bool>>& { return m_matrix; }

    // Note: this does not necessarily imply the whole colouring is valid
    auto recolour(int vertex, colour colour) -> bool {
        for (int neighbour : std::ranges::iota_view{0uz, m_matrix.size()}) {
            if (neighbour == vertex) continue;
            bool connected = m_matrix[vertex][neighbour];
            int neighbour_colour = m_colouring[neighbour];
            if (connected && colour == neighbour_colour) return false;
        }

        m_colouring[vertex] = colour;
        return true;
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

class NaiveMetropolisRunner {
   private:
    ColouredGraph& m_graph;
    std::vector<std::vector<colour>> m_hist;
    std::mt19937 m_vertex_gen{std::random_device{}()};
    std::mt19937 m_colour_gen{std::random_device{}()};
    std::uniform_int_distribution<> m_vertex_dist;
    std::uniform_int_distribution<> m_colour_dist;

    auto NaiveMetropolis() -> bool {
        auto result = m_graph.recolour(m_vertex_dist(m_vertex_gen), m_colour_dist(m_colour_gen));
        m_hist.emplace_back(m_graph.get_colouring());
        return result;
    }

   public:
    explicit NaiveMetropolisRunner(ColouredGraph& graph, size_t reps, size_t degree,
                                   colour n_colours, JsonlWriter& writer)
        : m_graph(graph) {
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        m_colour_dist = std::uniform_int_distribution<>(0, n_colours - 1);
        for (size_t i : std::ranges::iota_view{0uz, reps}) NaiveMetropolis();
        writer.write("graph", m_graph.get_adjacency(), "colourings:", m_hist, "nv",
                     graph.num_vertices(), "d", degree, "k", n_colours);
    }
};

class MiddletonBulsecoRunner {
   private:
    ColouredGraph& m_graph;
    std::vector<std::vector<colour>> m_hist;
    // keep track of how many of each colour
    std::vector<uint_fast32_t> m_colour_frequency{};
    std::mt19937 m_vertex_gen{std::random_device{}()};
    std::mt19937 m_colour_gen{std::random_device{}()};
    std::uniform_int_distribution<> m_vertex_dist;

    auto select_colour() -> colour {
        auto weights = m_colour_frequency | std::views::transform([this](uint_fast32_t k) {
                           return m_graph.num_vertices() - k;
                       });
        
        std::discrete_distribution<> colour_dist{weights.begin(),
                                                 weights.end()};
        return static_cast<colour>(colour_dist(m_colour_gen));
    }

    auto MiddletonBulseco() -> bool {
        auto selected_colour = select_colour();
        auto selected_vertex = m_vertex_dist(m_vertex_gen);

        auto old_colour = m_graph.get_colouring()[selected_vertex];
        auto result = m_graph.recolour(selected_vertex, selected_colour);
        if (result) {
            m_colour_frequency[old_colour]--;
            m_colour_frequency[selected_colour]++;
        }

        m_hist.emplace_back(m_graph.get_colouring());
        return result;
    }

   public:
    explicit MiddletonBulsecoRunner(ColouredGraph& graph, size_t reps, size_t degree,
                                    colour n_colours, JsonlWriter& writer)
        : m_graph(graph) {
        // usual setup
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        // initialise colour frequency from first colouring
        for (colour c : graph.get_colouring()) {
            m_colour_frequency[c]++;
        }

        for (size_t i : std::ranges::iota_view{0uz, reps}) MiddletonBulseco();
        writer.write("colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
                     n_colours);
    }
};


