
# CONSENSUS LAB - WEEK 4, DAY 1
# Experiment 12: Repeated Fork Rate Experiments

import csv
import math
import random
import statistics
from pathlib import Path


NETWORK_DELAYS = [0.1, 0.5, 1.0, 3.0, 5.0]
REPETITIONS = 10
TRIALS_PER_REPETITION = 1000
AVERAGE_MINING_TIME = 10.0
BASE_SEED = 42


def simulate_repetition(delay, seed):
    rng = random.Random(seed)
    forks = 0

    for _ in range(TRIALS_PER_REPETITION):
        bob_mining_time = rng.expovariate(
            1.0 / AVERAGE_MINING_TIME
        )

        if bob_mining_time < delay:
            forks += 1

    return forks / TRIALS_PER_REPETITION * 100


def run_experiments():
    all_results = []
    summary = []

    print("=== REPEATED FORK RATE EXPERIMENT ===")
    print(f"Repetitions: {REPETITIONS}")
    print(f"Trials per repetition: {TRIALS_PER_REPETITION}")
    print()

    for delay in NETWORK_DELAYS:
        rates = []

        for repetition in range(REPETITIONS):
            # Unique seed for each delay and repetition
            seed = BASE_SEED + repetition + (
                NETWORK_DELAYS.index(delay) * REPETITIONS
            )

            rate = simulate_repetition(delay, seed)
            rates.append(rate)

            all_results.append({
                "network_delay_seconds": delay,
                "repetition": repetition + 1,
                "seed": seed,
                "fork_rate_percent": round(rate, 2)
            })

        mean_rate = statistics.mean(rates)
        std_dev = statistics.stdev(rates)

        theoretical_rate = (
            1 - math.exp(-delay / AVERAGE_MINING_TIME)
        ) * 100

        summary.append({
            "network_delay_seconds": delay,
            "mean_fork_rate_percent": round(mean_rate, 3),
            "std_dev_percent": round(std_dev, 3),
            "theoretical_rate_percent": round(
                theoretical_rate, 3
            )
        })

        print(
            f"Delay: {delay:>4.1f}s | "
            f"Mean: {mean_rate:>6.2f}% | "
            f"Std Dev: {std_dev:>5.2f} | "
            f"Theory: {theoretical_rate:>6.2f}%"
        )

    return all_results, summary


def save_csv(filename, rows):
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / filename

    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {output_file}")


def main():
    all_results, summary = run_experiments()

    print("\n=== SAVING RESULTS ===")

    save_csv(
        "fork_rate_repeated.csv",
        all_results
    )

    save_csv(
        "fork_rate_summary.csv",
        summary
    )

    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
