# Assignment 6: Medians and Order Statistics & Elementary Data Structures

**Course:** CS Master's Program — University of the Cumberlands  
**Author:** Aashish

---

## Overview

This repository contains implementations and analysis for two core algorithmic topics:

- **Part 1:** Selection algorithms for finding the k-th smallest element (order statistics)
- **Part 2:** Elementary data structures implemented from scratch in Python

---

## Repository Structure

```
├── selection_algorithms.py    # Part 1: Median of Medians & Randomized Quickselect
├── empirical_analysis.py      # Part 1: Benchmarking and chart generation
├── data_structures.py         # Part 2: Arrays, Stacks, Queues, Linked Lists, Trees
├── performance_chart.png      # Empirical comparison chart
├── report.docx                # Detailed analysis report
└── README.md                  # This file
```

---

## How to Run

### Prerequisites
- Python 3.8+
- `matplotlib` (for chart generation): `pip install matplotlib`

### Part 1: Selection Algorithms

```bash
# Run correctness verification tests
python selection_algorithms.py

# Run empirical benchmarks and generate performance chart
python empirical_analysis.py
```

### Part 2: Data Structures

```bash
# Run interactive demo of all data structures
python data_structures.py
```

---

## Summary of Findings

### Part 1: Selection Algorithms

| Algorithm | Worst-Case Time | Expected Time | Space |
|-----------|----------------|---------------|-------|
| Median of Medians | O(n) | O(n) | O(n) |
| Randomized Quickselect | O(n²) | O(n) | O(n) |

**Key observations from empirical analysis:**
- Randomized Quickselect is consistently **1.5–2.5x faster** than Median of Medians in practice due to lower constant factors.
- Both algorithms scale linearly with input size across all tested distributions.
- The three-way partition handles duplicate elements efficiently in both implementations.
- Median of Medians pays a constant-factor overhead for its worst-case guarantee, which is rarely needed in practice.

### Part 2: Data Structures

| Data Structure | Access | Insert (head/end) | Delete | Search |
|---------------|--------|-------------------|--------|--------|
| Dynamic Array | O(1) | O(n) / O(1)* | O(n) | O(n) |
| Stack | O(1) top | O(1)* push | O(1) pop | O(n) |
| Queue (circular) | O(1) front | O(1)* enqueue | O(1) dequeue | O(n) |
| Singly Linked List | O(n) | O(1) / O(n) | O(n) | O(n) |

*Amortized

---

## Design Decisions

- **Three-way partitioning** is used in both selection algorithms to correctly and efficiently handle arrays with duplicate elements.
- **Circular buffer** is used for the Queue to achieve O(1) dequeue without shifting elements.
- **Dynamic resizing** (double on full, halve on quarter-full) is used in the Dynamic Array and Queue for amortized O(1) operations.
- All implementations include comprehensive docstrings, edge case handling, and `__repr__` methods for easy debugging.
