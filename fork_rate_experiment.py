
# CONSENSUS LAB - WEEK 3, DAY 4
# Experiment 10: Network Delay vs Fork Rate

import csv
import math
import random
from pathlib import Path


# Experiment settings
NETWORK_DELAYS = [0.1, 0.5, 1.0, 3.0, 5.0]
TRIALS_PER_DELAY = 1000

# Bob's average time to discover a block
AVERAGE_MINING_TIME = 10.0

# Fixed seed makes results reproducible
RANDOM_SEED = 42


def simulate_trial(network_delay, rng):
    """
    Alice mines at t=0.

    Bob continues mining until Alice's block arrives.
    A competing block occurs if Bob mines first.
    """

    bob_mining_time = rng.expovariate(
        1.0 / AVERAGE_MINING_TIME
    )

    fork_occurred = bob_mining_time < network_delay

    return fork_occurred, bob_mining_time


def run_experiment():
    rng = random.Random(RANDOM_SEED)
    results = []

    print("=== CONSENSUS LAB: FORK RATE EXPERIMENT ===")
    print(f"Trials per delay: {TRIALS_PER_DELAY}")
    print(f"Average Bob mining time: {AVERAGE_MINING_TIME}s")
    print()

    for delay in NETWORK_DELAYS:
        forks = 0

        for _ in range(TRIALS_PER_DELAY):
            fork, mining_time = simulate_trial(delay, rng)

            if fork:
                forks += 1

        fork_rate = forks / TRIALS_PER_DELAY * 100

        # Expected probability under exponential mining
        theoretical_rate = (
            1 - math.exp(-delay / AVERAGE_MINING_TIME)
        ) * 100

        results.append({
            "network_delay_seconds": delay,
            "trials": TRIALS_PER_DELAY,
            "forks": forks,
            "fork_rate_percent": round(fork_rate, 2),
            "theoretical_rate_percent": round(
                theoretical_rate, 2
            )
        })

        print(
            f"Delay: {delay:>4.1f}s | "
            f"Forks: {forks:>4} | "
            f"Fork rate: {fork_rate:>5.1f}% | "
            f"Theory: {theoretical_rate:>5.1f}%"
        )

    return results


def save_results(results):
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "fork_rate_experiment.csv"

    with output_file.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "network_delay_seconds",
                "trials",
                "forks",
                "fork_rate_percent",
                "theoretical_rate_percent"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_file}")


def main():
    results = run_experiment()
    save_results(results)

    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
