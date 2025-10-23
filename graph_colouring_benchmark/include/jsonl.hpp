// i apologise to anyone trying to read this file

#pragma once

#include <concepts>
#include <fstream>
#include <utility>
#include <vector>

struct escape_string_fn {
    template <std::ranges::range R>
    auto operator()(R&& r) const {
        std::string result;
        for (char c : r) {
            switch (c) {
                case '\\':
                    result.push_back('\\');
                    result.push_back('\\');
                    break;
                case '\"':
                    result.push_back('\\');
                    result.push_back('\"');
                    break;
                case '\n':
                    result.push_back('\\');
                    result.push_back('n');
                    break;
                case '\t':
                    result.push_back('\\');
                    result.push_back('t');
                    break;
                default:
                    result.push_back(c);
                    break;
            }
        }
        return result;
    }

    template <std::ranges::range R>
    friend auto operator|(R&& r, const escape_string_fn& fn) {
        return fn(std::forward<R>(r));
    }
};

inline constexpr escape_string_fn escape_string;

class JsonlWriter {
   private:
    std::ofstream m_out{};

    void write(std::string_view s) { m_out << '"' << (s | escape_string) << '"'; }
    void write(const char* s) { write(std::string_view{s}); }

    template <typename T>
        requires std::integral<T>
    void write(T t) {
        m_out << t;
    }

    template <typename T>
    requires (!std::same_as<T, char>)
    void write(const std::vector<T>& v) {
        m_out << '[';
        bool first = true;
        for (T e : v) {
            if (!first) m_out << ',';
            first = false;
            write(e);
        }
        m_out << ']';
    }

    void process(bool first) {}

    void process(bool first, auto key, auto value, auto... rest) {
        if (!first) m_out << ',';
        write(key);
        m_out << ':';
        write(value);
        process(false, rest...);
    }

   public:
    void write(auto... data) {
        bool first = true;

        m_out << '{';

        process(true, data...);

        m_out << "}\n";
    }

    explicit JsonlWriter(std::ofstream&& ofstream) : m_out{std::move(ofstream)} {}
};
