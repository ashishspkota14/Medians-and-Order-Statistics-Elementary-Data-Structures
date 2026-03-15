"""
Empirical Analysis of Selection Algorithms
===========================================
Compares the running time of Median of Medians vs Randomized Quickselect
across different input sizes and distributions.

Generates a performance comparison chart saved as PNG.
"""

import time
import random
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from selection_algorithms import median_of_medians, randomized_quickselect


def generate_input(size, distribution):
    """Generate test arrays with specific distributions."""
    if distribution == "random":
        return [random.randint(0, size * 10) for _ in range(size)]
    elif distribution == "sorted":
        return list(range(size))
    elif distribution == "reverse_sorted":
        return list(range(size, 0, -1))
    elif distribution == "duplicates":
        return [random.choice(range(10)) for _ in range(size)]
    else:
        raise ValueError(f"Unknown distribution: {distribution}")


def benchmark(func, arr, k, trials=5):
    """Measure average execution time over multiple trials."""
    times = []
    for _ in range(trials):
        arr_copy = list(arr)
        start = time.perf_counter()
        func(arr_copy, k)
        end = time.perf_counter()
        times.append(end - start)
    return statistics.mean(times)


def run_empirical_analysis():
    """Run the full empirical comparison and generate charts."""
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    distributions = ["random", "sorted", "reverse_sorted", "duplicates"]
    dist_labels = {
        "random": "Random",
        "sorted": "Sorted",
        "reverse_sorted": "Reverse Sorted",
        "duplicates": "Many Duplicates"
    }

    results = {dist: {"mom": [], "rqs": []} for dist in distributions}

    print("=" * 60)
    print("EMPIRICAL ANALYSIS")
    print("=" * 60)
    print(f"{'Size':<10} {'Distribution':<16} {'MoM (ms)':<14} {'RQS (ms)':<14} {'Ratio':<8}")
    print("-" * 62)

    for dist in distributions:
        for size in sizes:
            arr = generate_input(size, dist)
            k = size // 2  # Always find the median

            mom_time = benchmark(median_of_medians, arr, k) * 1000  # ms
            rqs_time = benchmark(randomized_quickselect, arr, k) * 1000

            results[dist]["mom"].append(mom_time)
            results[dist]["rqs"].append(rqs_time)

            ratio = mom_time / rqs_time if rqs_time > 0 else float('inf')
            print(f"{size:<10} {dist_labels[dist]:<16} {mom_time:<14.3f} {rqs_time:<14.3f} {ratio:<8.2f}")
        print()

    # Generate charts
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Selection Algorithm Performance Comparison", fontsize=16, fontweight='bold')

    for idx, dist in enumerate(distributions):
        ax = axes[idx // 2][idx % 2]
        ax.plot(sizes, results[dist]["mom"], 'o-', label="Median of Medians",
                color='#2196F3', linewidth=2, markersize=5)
        ax.plot(sizes, results[dist]["rqs"], 's-', label="Randomized Quickselect",
                color='#FF5722', linewidth=2, markersize=5)
        ax.set_title(f'{dist_labels[dist]} Distribution', fontsize=13, fontweight='bold')
        ax.set_xlabel('Input Size (n)')
        ax.set_ylabel('Time (ms)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig('performance_chart.png', dpi=150, bbox_inches='tight')
    print("Chart saved to performance_chart.png")
    plt.close()

    return results


if __name__ == "__main__":
    run_empirical_analysis()