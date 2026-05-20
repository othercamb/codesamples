/*
 * Count Pairs in a Range
 *
 * Demonstrates three approaches to counting/finding pairs of integers
 * within a given range [low, high]. A "pair" is an unordered combination
 * of two distinct values (i, j) where i < j.
 *
 * Example: range [1, 3] has 3 pairs: (1,2), (1,3), (2,3)
 */

#include <stdio.h>
#include <stdlib.h>

/*
 * Count all unique pairs (i, j) where i < j and both are in [low, high].
 *
 * Uses the combinatorics formula C(n, 2) = n * (n - 1) / 2,
 * where n is the number of elements in the range.
 * This is O(1) — no iteration needed.
 *
 * Example: [1, 5] has 5 elements, so C(5,2) = 5*4/2 = 10 pairs.
 */
int count_pairs(int low, int high)
{
    int n = high - low + 1;  /* number of elements in the range */
    if (n <= 1) return 0;    /* need at least 2 elements to form a pair */
    return n * (n - 1) / 2;  /* combination formula: choose 2 from n */
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
int count_pairs_with_sum(int low, int high, int target)
{
    int count = 0;
    for (int i = low; i <= high; i++) {
        int j = target - i;                   /* j that satisfies i + j == target */
        if (j > i && j >= low && j <= high)   /* distinct, ordered, and in range */
            count++;
    }
    return count;
}

/*
 * Struct to hold a pair of integers.
 * C has no built-in pair/tuple type, so we define one.
 */
typedef struct {
    int a;
    int b;
} Pair;

/*
 * Enumerate and return all pairs in [low, high].
 *
 * Uses a nested loop: outer picks i, inner picks j from i+1 onward.
 * This guarantees i < j and avoids duplicate pairs.
 * Runs in O(n^2) and produces C(n,2) pairs.
 *
 * Parameters:
 *   low, high  — the inclusive bounds of the range
 *   out_count   — output: will be set to the number of pairs found
 *
 * Returns: dynamically allocated array of Pair.
 *          Caller is responsible for calling free().
 *          Returns NULL if no pairs and sets *out_count = 0.
 */
Pair* enumerate_pairs(int low, int high, int* out_count)
{
    int n = high - low + 1;
    if (n <= 1) {
        *out_count = 0;
        return NULL;
    }

    int total = n * (n - 1) / 2;          /* C(n,2) — total number of pairs */
    Pair* pairs = malloc((size_t)total * sizeof(Pair));
    if (pairs == NULL) {                 /* malloc failed */
        *out_count = 0;
        return NULL;
    }

    int idx = 0;
    for (int i = low; i <= high; i++)           /* pick the first element */
        for (int j = i + 1; j <= high; j++)     /* pick the second element (always after i) */
            pairs[idx++] = (Pair){i, j};        /* compound literal assignment */

    *out_count = total;
    return pairs;
}

int main(void)
{
    int low = 1, high = 5;

    /* --- Demo 1: Total pair count using the O(1) formula --- */
    printf("Range [%d, %d]\n", low, high);
    printf("Total pairs: %d\n\n", count_pairs(low, high));

    /* --- Demo 2: Pairs that sum to a specific target --- */
    int target = 6;
    printf("Pairs with sum %d: %d\n\n",
           target, count_pairs_with_sum(low, high, target));

    /* --- Demo 3: Full enumeration of all pairs --- */
    int count = 0;
    Pair* pairs = enumerate_pairs(low, high, &count);
    printf("All pairs:\n");
    for (int k = 0; k < count; k++)
        printf("  (%d, %d)\n", pairs[k].a, pairs[k].b);
    free(pairs);  /* caller must free the allocated memory */

    return 0;
}
