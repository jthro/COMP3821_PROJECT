#pragma once

#include <algorithm>
#include <array>
#include <numeric>
#include <optional>
#include <ranges>
#include <tuple>

struct ColourSuccess {};
// Generate a sequence of integer pairs corresponding to upper triangular (minus the diagonal)
// indices of a square matrix
template <int n>
auto upper_triangular_range() {
    return std::views::cartesian_product(std::ranges::iota_view{0, n},
                                         std::ranges::iota_view{0, n}) |
           std::views::filter(
               [](std::tuple<int, int> pair) { return std::get<1>(pair) > std::get<0>(pair); });
}

template <int nV>
struct AdjacencyMatrix : std::array<std::array<bool, nV>, nV> {
    auto compute_num_edges() const -> int {
        // Read as:
        // Take a sequence of ints corresponding to upper triangular (minus the diagonal indices) ->
        // transform them into 1 if connected, 0 otherwise -> sum
        auto r =
            upper_triangular_range<nV>() | std::views::transform([this](std::tuple<int, int> pair) {
                return static_cast<int>((*this)[std::get<0>(pair)][std::get<1>(pair)]);
            });
        return std::accumulate(r.begin(), r.end(), 0);
    }
};

template <int nV>
class ColouredGraph {
   private:
    AdjacencyMatrix<nV> m_matrix{};
    std::array<int, nV> m_colouring{};
    const int m_num_edges;

   public:
    template <typename T>
    explicit ColouredGraph(T&& matrix, std::array<int, nV> colouring)
        : m_matrix{std::forward<T>(matrix)},
          m_colouring{std::move(colouring)},
          m_num_edges{m_matrix.compute_num_edges()} {}

    auto get_colouring() const -> const std::array<int, nV>& { return m_colouring; }

    // Returns std::nullopt if the colouring failed
    // Returns marker struct if the colouring succeeded
    // Note: this does not necessarily imply the whole colouring is valid
    auto recolour(int vertex, int colour) -> std::optional<ColourSuccess> {
        for (int neighbour : std::ranges::iota_view{0, nV}) {
            bool connected = m_matrix[vertex][neighbour];
            int neighbour_colour = m_colouring[neighbour];
            if (connected && colour == neighbour_colour) return std::nullopt;

            m_colouring[vertex] = colour;
            return ColourSuccess{};
        }
    }

    auto num_vertices() const -> int { return nV; }

    auto num_edges() const -> const int& { return m_num_edges; }

    auto valid_colouring() -> bool {
        auto r =
            upper_triangular_range<nV>() | std::views::transform([this](std::tuple<int, int> pair) {
                return (!(m_matrix[std::get<0>(pair)][std::get<1>(pair)] &&
                          m_colouring[std::get<0>(pair)] == m_colouring[std::get<1>(pair)]));
            });
        return std::accumulate(r.begin(), r.end(), true, [](bool a, bool b) { return a && b; });
    }
};
