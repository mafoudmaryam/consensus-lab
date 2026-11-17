
# CONSENSUS LAB - FINAL STATISTICAL ANALYSIS

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    results_dir = Path("results")
    input_file = results_dir / "fork_rate_repeated.csv"

    grouped = defaultdict(list)

    with input_file.open(newline="") as file:
        for row in csv.DictReader(file):
            delay = float(row["network_delay_seconds"])
            rate = float(row["fork_rate_percent"])
            grouped[delay].append(rate)

    delays = []
    means = []
    lower_bounds = []
    upper_bounds = []
    theory = []
    output_rows = []

    # Two-sided 95% Student t critical value, df=9
    t_critical = 2.262

    print("=== FINAL STATISTICAL RESULTS ===")

    for delay in sorted(grouped):
        rates = grouped[delay]
        n = len(rates)

        mean = statistics.mean(rates)
        std = statistics.stdev(rates)

        margin = t_critical * std / math.sqrt(n)
        lower = mean - margin
        upper = mean + margin

        expected = (1 - math.exp(-delay / 10)) * 100

        delays.append(delay)
        means.append(mean)
        lower_bounds.append(lower)
        upper_bounds.append(upper)
        theory.append(expected)

        output_rows.append({
            "delay_seconds": delay,
            "mean_percent": round(mean, 3),
            "std_dev_percentage_points": round(std, 3),
            "ci_lower_percent": round(lower, 3),
            "ci_upper_percent": round(upper, 3),
            "theoretical_percent": round(expected, 3)
        })

        print(
            f"Delay {delay:.1f}s: "
            f"Mean={mean:.2f}%, "
            f"95% CI=[{lower:.2f}%, {upper:.2f}%]"
        )

    output_csv = results_dir / "final_statistics.csv"

    with output_csv.open("w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=list(output_rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(output_rows)

    plt.figure(figsize=(9, 5.5))

    plt.plot(
        delays, means,
        marker="o",
        label="Simulation Mean"
    )

    plt.fill_between(
        delays, lower_bounds, upper_bounds,
        alpha=0.2,
        label="95% Confidence Interval"
    )

    plt.plot(
        delays, theory,
        linestyle="--",
        label="Theoretical Prediction"
    )

    plt.xlabel("Network Delay (seconds)")
    plt.ylabel("Competing-Block Probability (%)")
    plt.title("Network Delay and Competing-Block Probability")
    plt.xticks(delays)
    plt.ylim(bottom=0)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        results_dir / "final_statistics_graph.png",
        dpi=300
    )
    plt.savefig(
        results_dir / "final_statistics_graph.pdf"
    )

    plt.close()

    print("\nSaved final statistics and graphs.")
    print("EXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
