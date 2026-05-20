/*
 * Count Pairs in a Range
 *
 * Demonstrates three approaches to counting/finding pairs of integers
 * within a given range [low, high]. A "pair" is an unordered combination
 * of two distinct values (i, j) where i < j.
 *
 * Example: range [1, 3] has 3 pairs: (1,2), (1,3), (2,3)
 */

#include <iostream>
#include <vector>
#include <utility>

/*
 * Count all unique pairs (i, j) where i < j and both are in [low, high].
 *
 * Uses the combinatorics formula C(n, 2) = n * (n - 1) / 2,
 * where n is the number of elements in the range.
 * This is O(1) — no iteration needed.
 *
 * Example: [1, 5] has 5 elements, so C(5,2) = 5*4/2 = 10 pairs.
 */
int count_pairs(int low, int high) {
    int n = high - low + 1;  // number of elements in the range
    if (n <= 1) return 0;    // need at least 2 elements to form a pair
    return n * (n - 1) / 2;  // combination formula: choose 2 from n
}

/*
 * Count pairs (i, j) where i < j, i + j == target, and both are in [low, high].
 *
 * For each i in the range, compute j = target - i. The pair is valid if:
 *   - j > i    (avoid duplicates and ensure i != j)
 *   - j is within [low, high]
 *
 * This runs in O(n) where n is the range size.
 *
 * Example: [1, 5] with target 6 → (1,5) and (2,4) → count = 2.
 */
int count_pairs_with_sum(int low, int high, int target) {
    int count = 0;
    for (int i = low; i <= high; i++) {
        int j = target - i;          // the value j that would satisfy i + j == target
        if (j > i && j >= low && j <= high) {  // j must be distinct, after i, and in range
            count++;
        }
    }
    return count;
}

/*
 * Enumerate and return all pairs in [low, high] as a vector.
 *
 * Uses a nested loop: outer picks i, inner picks j from i+1 onward.
 * This guarantees i < j and avoids duplicate pairs like (3,1) when (1,3) exists.
 * Runs in O(n^2) and produces C(n,2) pairs.
 */
std::vector<std::pair<int, int>> enumerate_pairs(int low, int high) {
    std::vector<std::pair<int, int>> pairs;
    for (int i = low; i <= high; i++) {       // pick the first element
        for (int j = i + 1; j <= high; j++) { // pick the second element (always after i)
            pairs.emplace_back(i, j);         // add the pair to the result
        }
    }
    return pairs;
}

int main() {
    int low = 1, high = 5;

    // --- Demo 1: Total pair count using the O(1) formula ---
    std::cout << "Range [" << low << ", " << high << "]\n";
    std::cout << "Total pairs: " << count_pairs(low, high) << "\n\n";

    // --- Demo 2: Pairs that sum to a specific target ---
    int target = 6;
    std::cout << "Pairs with sum " << target << ": "
              << count_pairs_with_sum(low, high, target) << "\n\n";

    // --- Demo 3: Full enumeration of all pairs ---
    auto pairs = enumerate_pairs(low, high);
    std::cout << "All pairs:\n";
    for (auto [a, b] : pairs) {  // structured binding (C++17) unpacks each pair
        std::cout << "  (" << a << ", " << b << ")\n";
    }

    return 0;
}
