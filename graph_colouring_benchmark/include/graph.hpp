
#pragma once

#include <algorithm>
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <numeric>
#include <print>
#include <queue>
#include <random>
#include <ranges>
#include <set>
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

inline auto cursed_adjacency_matrix(size_t n_v) -> AdjacencyMatrix {
    std::vector<std::vector<bool>> m(n_v, std::vector<bool>(n_v, false));
    std::fill(m[0].begin(), m[0].end(), true);
    for (std::size_t i = 0; i < n_v; i++) {
        std::println("{}", i);
        m[i][0] = true;
        m[i][i] = true;
    }

    return static_cast<AdjacencyMatrix>(m);
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

    static auto generate_colouring(size_t n, colour k) -> std::vector<colour> {
        std::random_device rd;
        std::mt19937 gen{rd()};
        std::uniform_int_distribution<> colour_distribution(0, k - 1);

        std::vector<colour> colouring{};
        for (auto i : std::ranges::iota_view{0uz, n}) {
            colouring.emplace_back(colour_distribution(gen));
        }

        return colouring;
    }

    template <typename T>
    explicit ColouredGraph(T&& matrix, colour n_colours)
        : m_matrix{std::forward<T>(matrix)},
          m_num_edges{m_matrix.compute_num_edges()},
          m_colouring{generate_colouring(matrix.size(), n_colours)} {}

    template <typename T, typename U>
    explicit ColouredGraph(T&& matrix, U&& colouring)
        : m_matrix{std::forward<T>(matrix)},
          m_colouring{std::forward<U>(colouring)},
          m_num_edges{m_matrix.compute_num_edges()} {}

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
    std::mt19937 m_vertex_gen{};
    std::mt19937 m_colour_gen{};
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
        : m_graph(graph),
          m_vertex_gen{std::random_device{}()},
          m_colour_gen{std::random_device{}()} {
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        m_colour_dist = std::uniform_int_distribution<>(0, n_colours - 1);
        for (size_t i : std::ranges::iota_view{0uz, reps}) NaiveMetropolis();
        writer.write("chain", "naive-metropolis", "graph", m_graph.get_adjacency(),
                     "colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
                     n_colours);
    }

    explicit NaiveMetropolisRunner(ColouredGraph& graph, size_t reps, size_t degree,
                                   colour n_colours, std::mt19937& vertex_seed,
                                   std::mt19937& colour_seed, JsonlWriter& writer)
        : m_graph(graph), m_vertex_gen{vertex_seed}, m_colour_gen{colour_seed} {
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        m_colour_dist = std::uniform_int_distribution<>(0, n_colours - 1);
        for (size_t i : std::ranges::iota_view{0uz, reps}) NaiveMetropolis();
        writer.write("chain", "naive-metropolis", "graph", m_graph.get_adjacency(),
                     "colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
                     n_colours);
    }

    explicit NaiveMetropolisRunner(ColouredGraph& graph, size_t reps, std::string graph_type,
                                   colour n_colours, std::mt19937& vertex_seed,
                                   std::mt19937& colour_seed, JsonlWriter& writer)
        : m_graph(graph), m_vertex_gen{vertex_seed}, m_colour_gen{colour_seed} {
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        m_colour_dist = std::uniform_int_distribution<>(0, n_colours - 1);
        for (size_t i : std::ranges::iota_view{0uz, reps}) NaiveMetropolis();
        writer.write("chain", "naive-metropolis", "graph", m_graph.get_adjacency(),
                     "colourings:", m_hist, "nv", graph.num_vertices(), "shape", graph_type.c_str(),
                     "k", n_colours);
    }
};

class MiddletonBulsecoRunner {
   private:
    ColouredGraph& m_graph;
    std::vector<std::vector<colour>> m_hist;
    // keep track of how many of each colour
    std::vector<uint_fast32_t> m_colour_frequency{};
    std::mt19937 m_vertex_gen{};
    std::mt19937 m_colour_gen{};
    std::uniform_int_distribution<> m_vertex_dist;

    auto select_colour() -> colour {
        auto weights = m_colour_frequency | std::views::transform([this](uint_fast32_t k) {
                           return m_graph.num_vertices() - k;
                       });

        std::discrete_distribution<> colour_dist{weights.begin(), weights.end()};
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
        : m_graph(graph),
          m_colour_frequency(n_colours),
          m_vertex_gen{std::random_device{}()},
          m_colour_gen{std::random_device{}()} {
        // usual setup
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        // initialise colour frequency from first colouring
        for (colour c : graph.get_colouring()) {
            m_colour_frequency[c]++;
        }

        for (size_t i : std::ranges::iota_view{0uz, reps}) MiddletonBulseco();
        writer.write("chain", "middleton-bulseco", "graph", m_graph.get_adjacency(),
                     "colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
                     n_colours);
    }

    // copies seed by value
    explicit MiddletonBulsecoRunner(ColouredGraph& graph, size_t reps, size_t degree,
                                    colour n_colours, std::mt19937& vertex_seed,
                                    std::mt19937& colour_seed, JsonlWriter& writer)
        : m_graph(graph),
          m_colour_frequency(n_colours),
          m_vertex_gen{vertex_seed},
          m_colour_gen{colour_seed} {
        // usual setup
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        // initialise colour frequency from first colouring
        for (colour c : graph.get_colouring()) {
            m_colour_frequency[c]++;
        }

        for (size_t i : std::ranges::iota_view{0uz, reps}) MiddletonBulseco();
        writer.write("chain", "middleton-bulseco", "graph", m_graph.get_adjacency(),
                     "colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
                     n_colours);
    }

    explicit MiddletonBulsecoRunner(ColouredGraph& graph, size_t reps, std::string graph_type,
                                    colour n_colours, std::mt19937& vertex_seed,
                                    std::mt19937& colour_seed, JsonlWriter& writer)
        : m_graph(graph),
          m_colour_frequency(n_colours),
          m_vertex_gen{vertex_seed},
          m_colour_gen{colour_seed} {
        // usual setup
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        // initialise colour frequency from first colouring
        for (colour c : graph.get_colouring()) {
            m_colour_frequency[c]++;
        }

        for (size_t i : std::ranges::iota_view{0uz, reps}) MiddletonBulseco();
        writer.write("chain", "middleton-bulseco", "graph", m_graph.get_adjacency(), "colourings",
                     m_hist, "nv", graph.num_vertices(), "shape", graph_type.c_str(), "k",
                     n_colours);
    }
};

class FlipDynamicsRunner {
   private:
    ColouredGraph& m_graph;
    std::vector<std::vector<colour>> m_hist;
    std::mt19937 m_vertex_gen{std::random_device{}()};
    std::mt19937 m_colour_gen{std::random_device{}()};
    std::uniform_int_distribution<> m_vertex_dist;
    std::uniform_int_distribution<> m_colour_dist;

    std::vector<int> neighbours(int u, ColouredGraph& graph) const {
        std::vector<int> neighbours(int u);
        std::vector<int> neighbourList;
        for (int i = 0; i < graph.num_vertices(); i++) {
            if (graph.get_adjacency()[u][i] == 1) {
                neighbourList.push_back(i);
            }
        }
        return neighbourList;
    }

    auto Flip() -> bool {
        int Pl = 1;

        auto current = m_graph.get_colouring();

        int v = m_vertex_dist(m_vertex_gen);
        colour b = current[v];
        colour c = m_colour_dist(m_colour_gen);

        while (c == b) {
            c = m_colour_dist(m_colour_gen);
        }

        std::set<int> cluster;
        std::queue<int> queue;

        queue.push(v);
        cluster.insert(v);

        while (!queue.empty()) {
            int u = queue.front();
            queue.pop();
            colour u_colour = current[u];
            int target_colour;
            if (u_colour == b) {
                target_colour = c;
            } else {
                target_colour = b;
            }
            std::vector<int> neighbour = neighbours(u, m_graph);
            for (int n = 0; n < neighbour.size(); n++) {
                if (current[n] == target_colour && !(cluster.contains(n))) {
                    cluster.insert(n);
                    queue.push(n);
                }
            }
        }

        int l = cluster.size();
        bool accept = false;

        std::random_device rd;
        std::mt19937 gen{rd()};
        std::uniform_real_distribution<double> dist(0.0, 1.0);
        double r = dist(gen);

        if (l > 0 && r < double(Pl) / l) {
            accept = true;
            for (const auto& u : cluster) {
                if (current[u] == b) {
                    m_graph.recolour(u, c);
                } else {
                    m_graph.recolour(u, b);
                }
            }
        }

        m_hist.push_back(m_graph.get_colouring());
        return accept;
    }

   public:
    explicit FlipDynamicsRunner(ColouredGraph& graph, size_t reps, size_t degree, colour n_colours,
                                JsonlWriter& writer)
        : m_graph(graph) {
        m_hist.emplace_back(m_graph.get_colouring());
        m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
        m_colour_dist = std::uniform_int_distribution<>(0, n_colours - 1);

        for (size_t i : std::ranges::iota_view{0uz, reps}) Flip();

        writer.write("chain", "flip-dynamics", "graph", m_graph.get_adjacency(),
                     "colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
                     n_colours);
    }
};

// class SussyBaka7Runner {
//     private:
//         ColouredGraph& m_graph;
//             std::vector<std::vector<colour>> m_hist;
//         std::mt19937 m_vertex_gen{std::random_device{}()};
//         // added a tie break
//         std::mt19937 m_tiebreak_gen{std::random_device[]()};
//         std::uniform_int_distribution<> m_vertex_dist;
//         std::vector<std::vector<int>> invalid_nautral;

//         void build_invalid_neutral() {
//             int n = m_graph.num_vertices();
//             auto& adj = m_graph.get_adjacency();
//             auto colouring = m_graph.get_adjacency();

//             invalid_neutral.assign(n, std::vector<int>(k, 0));
//         }
//         auto InvalidAlgo() -> bool {
//             std::vector<std::vector<colour>>> colours;

//             // IDK MAN

//             for (int i = 0; i m_graph.num_vertices(); i++) {

//             }
//         }

//     public:
//         explicit SussyBaka7Runner(
//             ColouredGraph& graph, size_t reps, size_t degree,
//             colour n_colours, JsonlWriter& writer)
//             : m_graph(graph)

//             {
//             m_hist.emplace_back(m_graph.get_colouring());
//             m_vertex_dist = std::uniform_int_distribution<>(0, graph.num_vertices() - 1);
//             m_colour_dist = std::uniform_int_distribution<>(0, n_colours - 1);

//             for (size_t i : std::ranges::iota_view{0uz, reps}) InvalidAlgo();

//             writer.write("chain", "sussy-baka-7", "graph", m_graph.get_adjacency(),
//                         "colourings:", m_hist, "nv", graph.num_vertices(), "d", degree, "k",
//                         n_colours);
//         }
// }
