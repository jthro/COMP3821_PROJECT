#include <cassert>
#include <cstddef>
#include <cstring>
#include <fstream>

struct TestData {
    size_t n_start;
    size_t n_stop;
    size_t n_step;

    double delta_start;
    double delta_stop;
    double delta_step;

    size_t delta_coeff_start;
    size_t delta_coeff_stop;
    size_t delta_coeff_step;

    size_t delta_constant_start;
    size_t delta_constant_stop;
    size_t delta_constant_step;

    size_t n_trials_per;

    TestData(std::ifstream file) {
        char l1[3];
        file >> l1;
        assert(!strcmp(l1, "n:"));

        file >> n_start;
        file >> n_stop;
        file >> n_step;

        char l2[7];
        file >> l2;
        assert(!strcmp(l2, "delta:"));

        file >> delta_start;
        file >> delta_stop;
        file >> delta_step;

        char l3[3];
        file >> l3;
        assert(!strcmp(l3, "k:"));

        file >> delta_coeff_start;
        file >> delta_constant_start;
        file >> delta_coeff_stop;
        file >> delta_constant_stop;
        file >> delta_coeff_step;
        file >> delta_constant_step;

        char l4[8];
        file >> l4;
        assert(!strcmp(l4, "trials:"));
        file >> n_trials_per;
    }
};
