#include <algorithm>
#include <array>
#include <print>
#include <ranges>
#include <random>


static std::random_device rd;
static std::mt19937 rng(rd());

struct Item {
    std::size_t id;
    std::size_t value;
    bool fit = false;

    void compute_fitness() {
        std::uniform_int_distribution<int> dist(0, 1);
        fit = dist(rng);
    }
};

constexpr std::array<Item, 10> create_items() {
    return {
        Item(0, 4), Item(1, 8), Item(2, 1), Item(3, 7),
        Item(4, 1), Item(5, 3), Item(6, 7), Item(7, 9),
        Item(8, 2), Item(9, 4),
    };
}

std::array<Item*, 3> get_random_elems(std::array<Item, 10>& items) {
    std::array<Item*, 3> elems = {};

    std::uniform_int_distribution<int> dist(0, 9);

    for (std::size_t i = 0; i < 3; i++) {
        elems.at(i) = &items.at(static_cast<std::size_t>(dist(rng)));
    }

    return elems;
}

void rotate_values(const std::array<Item*, 3>& elems) {
    std::size_t temp = elems.at(0)->value;
    elems.at(0)->value = elems.at(1)->value;
    elems.at(1)->value = elems.at(2)->value;
    elems.at(2)->value = temp;
}

void crossover(const std::array<Item*, 3>& elems) {
    std::size_t total = elems.at(0)->value + elems.at(1)->value + elems.at(2)->value;
    elems.at(0)->value = (total / 3) % std::numeric_limits<std::size_t>::max();
    elems.at(1)->value = total / 3;
    elems.at(2)->value = total / 3;
}

void mutate(const std::array<Item*, 3>& elems) {
    // Get a random number picking any bit in a size_t
    std::uniform_int_distribution<int> dist(0, sizeof(std::size_t) * 8);
    int bit = dist(rng);

    // Enable only the chosen bit in the set
    auto a = 1uz << bit;

    elems.at(0)->value += ~a;
    elems.at(1)->value += ~a;
    elems.at(2)->value += ~a;
}

// If over half of the elements are considered fit, we return true
bool not_fit_enough(std::array<Item, 10>& items) {
    auto count = std::count_if(
        items.begin(),
        items.end(),
        [](Item& i) {
            i.compute_fitness();
            return i.fit;
        }
    );

    return count >= 5;
}

int main() {
    std::println("Knapsack problem");
    std::println("----------------");
    auto items = create_items();
    auto random_elems = get_random_elems(items);

    do {
        rotate_values(random_elems);
        crossover(random_elems);
        mutate(random_elems);

    } while (not_fit_enough(items));

    auto print_item = [](Item i){ std::println("ID: {}, value: {}", i.id, i.value); };
    std::for_each(items.begin(), items.end(), print_item);
}
