"""
Part 1: Implementation and Analysis of Selection Algorithms
============================================================
This module implements two algorithms for finding the k-th smallest element:
1. Deterministic Selection (Median of Medians) - O(n) worst-case
2. Randomized Quickselect - O(n) expected time

Author: Aashish
Course: CS Master's Program - University of the Cumberlands
Assignment: 6 - Medians and Order Statistics & Elementary Data Structures
"""

import random


# =============================================================================
# Deterministic Selection: Median of Medians
# =============================================================================

def median_of_medians(arr, k):
    """
    Select the k-th smallest element using the Median of Medians algorithm.
    Guarantees O(n) worst-case time complexity.

    Parameters:
        arr (list): Input list of comparable elements.
        k (int): 1-based index of the desired order statistic (1 = minimum).

    Returns:
        The k-th smallest element in the array.

    Raises:
        ValueError: If k is out of valid range.
    """
    if not arr:
        raise ValueError("Array must not be empty.")
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}.")

    return _mom_select(list(arr), k)


def _mom_select(arr, k):
    """Internal recursive helper for Median of Medians selection."""
    n = len(arr)

    # Base case: small arrays can be sorted directly
    if n <= 5:
        return sorted(arr)[k - 1]

    # Step 1: Divide array into groups of 5 and find each group's median
    medians = []
    for i in range(0, n, 5):
        group = arr[i:i + 5]
        group.sort()
        medians.append(group[len(group) // 2])

    # Step 2: Recursively find the median of medians (pivot)
    pivot = _mom_select(medians, (len(medians) + 1) // 2)

    # Step 3: Partition array around the pivot (three-way partition for duplicates)
    low, equal, high = [], [], []
    for x in arr:
        if x < pivot:
            low.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            high.append(x)

    # Step 4: Recurse into the appropriate partition
    if k <= len(low):
        return _mom_select(low, k)
    elif k <= len(low) + len(equal):
        return pivot
    else:
        return _mom_select(high, k - len(low) - len(equal))


# =============================================================================
# Randomized Quickselect
# =============================================================================

def randomized_quickselect(arr, k):
    """
    Select the k-th smallest element using Randomized Quickselect.
    Achieves O(n) expected time complexity.

    Parameters:
        arr (list): Input list of comparable elements.
        k (int): 1-based index of the desired order statistic (1 = minimum).

    Returns:
        The k-th smallest element in the array.

    Raises:
        ValueError: If k is out of valid range.
    """
    if not arr:
        raise ValueError("Array must not be empty.")
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range for array of length {len(arr)}.")

    return _rand_select(list(arr), k)


def _rand_select(arr, k):
    """Internal recursive helper for Randomized Quickselect."""
    n = len(arr)

    # Base case
    if n == 1:
        return arr[0]

    # Step 1: Choose a random pivot
    pivot = arr[random.randint(0, n - 1)]

    # Step 2: Three-way partition (handles duplicates efficiently)
    low, equal, high = [], [], []
    for x in arr:
        if x < pivot:
            low.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            high.append(x)

    # Step 3: Recurse into the appropriate partition
    if k <= len(low):
        return _rand_select(low, k)
    elif k <= len(low) + len(equal):
        return pivot
    else:
        return _rand_select(high, k - len(low) - len(equal))


# =============================================================================
# Verification & Demo
# =============================================================================

def verify_algorithms():
    """Run correctness tests on both selection algorithms."""
    print("=" * 60)
    print("VERIFICATION TESTS")
    print("=" * 60)

    test_cases = [
        # (array, k, description)
        ([3, 1, 4, 1, 5, 9, 2, 6], 1, "Minimum element"),
        ([3, 1, 4, 1, 5, 9, 2, 6], 8, "Maximum element"),
        ([3, 1, 4, 1, 5, 9, 2, 6], 4, "Median (4th smallest)"),
        ([7, 7, 7, 7, 7], 3, "All duplicates"),
        ([1], 1, "Single element"),
        ([5, 3], 2, "Two elements"),
        (list(range(100, 0, -1)), 50, "Reverse sorted, median"),
        ([2, 2, 2, 1, 1, 3, 3, 3], 5, "Many duplicates"),
    ]

    all_passed = True
    for arr, k, desc in test_cases:
        expected = sorted(arr)[k - 1]
        mom_result = median_of_medians(arr, k)
        rqs_result = randomized_quickselect(arr, k)
        status = "PASS" if mom_result == expected == rqs_result else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  [{status}] {desc}: k={k}, expected={expected}, "
              f"MoM={mom_result}, RQS={rqs_result}")

    print(f"\n{'All tests passed!' if all_passed else 'Some tests FAILED!'}\n")
    return all_passed


if __name__ == "__main__":
    verify_algorithms()
