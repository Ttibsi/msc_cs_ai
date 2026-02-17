#include <algorithm>
#include <array>
#include <cstddef>
#include <print>
#include <random>
#include <set>
#include <vector>

std::random_device dev;
std::mt19937 rng(dev());

constexpr static int POP_SIZE = 1024;
static_assert(POP_SIZE % 2 == 0);
constexpr static std::array<std::array<int, 5>, 5> distances = {{
    {0, 4, 2, 8, 6},
    {4, 0, 2, 3, 9},
    {2, 2, 0, 3, 2},
    {6, 3, 3, 0, 9},
    {8, 9, 2, 9, 0}
}};

[[nodiscard]] constexpr std::array<int, 5> gen_solution() {
    std::array<int, 5> ret = {1,2,3,4,5};
    std::shuffle(ret.begin(), ret.end(), rng);
    return ret;
}

[[nodiscard]] constexpr int calculate_distance(const std::array<int, 5>* path) {
     auto set = std::set<int>(path->begin(), path->end());
     if (set.size() != 5) { return 0; }

     int ret = 0;
     // Go one less than the length of the array so we can look one ahead
     for (std::size_t i = 0; i < path->size() - 1; i++) {
         const std::array<int, 5>* inner = &distances.at(i);
         ret += inner->at(path->at(i + 1) - 1);
     }

     return ret;
}

// Tournament selection over every pair of elements.
// this should essentially halve the length of the population
[[nodiscard]] constexpr std::vector<std::array<int, 5>> selection(const std::vector<std::array<int, 5>>* pop) {
    std::vector<std::array<int, 5>> ret = {};
    ret.reserve(pop->size() / 2);

    for (std::size_t i = 0; i < pop->size() - 1; i +=2) {
        std::array<int, 5> a1 = pop->at(i);
        std::array<int, 5> a2 = pop->at(i + 1);
        const int a1_dist = calculate_distance(&a1);
        const int a2_dist = calculate_distance(&a2);
        ret.push_back((a1_dist > a2_dist ? a1 : a2));
    }

    return ret;
}

constexpr void crossover(std::vector<std::array<int, 5>>* pop) {
    for (std::size_t i = 0; i < pop->size() - 1; i += 2) {
        std::array<int, 5>* a1 = &pop->at(i);
        std::array<int, 5>* a2 = &pop->at(i + 1);
        std::array<int, 5> child1 = {
            a1->at(0), a1->at(1), a2->at(2), a2->at(3), a2->at(4)
        };

        std::array<int, 5> child2 = {
            a2->at(0), a2->at(1), a1->at(2), a1->at(3), a1->at(4)
        };

        auto set1 = std::set<int>(child1.begin(), child1.end());
        auto set2 = std::set<int>(child2.begin(), child2.end());
        if (set1.size() == 5 && set2.size() == 5) {
            pop->at(i) = child1;
            pop->at(i + 1) = child2;
        }
    }
}

constexpr void mutate(std::vector<std::array<int, 5>>* pop) {
    for (auto elem: *pop) {
        std::rotate(elem.begin(), elem.begin() + 2, elem.end());
    }
}

[[nodiscard]] constexpr bool fitness(const std::vector<std::array<int, 5>>* pop) {
    return pop->size() < 2;
}

int main() {
    std::vector<std::array<int, 5>> pop = {};
    pop.reserve(POP_SIZE);
    for (int i = 0; i < POP_SIZE; i++) {
        pop.push_back(gen_solution());
    }

    int iterations = 0;

    while (!fitness(&pop)) {
        iterations++;

        pop = selection(&pop);
        crossover(&pop);
        mutate(&pop);
    }

    std::println("Final path after {} iterations", iterations);
    std::print("[");
    std::for_each(pop.at(0).begin(), pop.at(0).end(), [](int i) { std::print(" {} ", i); });
    std::println("] (Cost: {})", calculate_distance(&pop.at(0)));
}
