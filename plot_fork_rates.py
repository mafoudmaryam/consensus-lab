
# CONSENSUS LAB - WEEK 3, DAY 5
# Experiment 11: Visualizing Fork Rates

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_results():
    file_path = Path("results/fork_rate_experiment.csv")

    if not file_path.exists():
        raise FileNotFoundError(
            "Results file not found. "
            "Run fork_rate_experiment.py first."
        )

    delays = []
    simulated_rates = []
    theoretical_rates = []

    with file_path.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            delays.append(
                float(row["network_delay_seconds"])
            )

            simulated_rates.append(
                float(row["fork_rate_percent"])
            )

            theoretical_rates.append(
                float(row["theoretical_rate_percent"])
            )

    return delays, simulated_rates, theoretical_rates


def create_graph():
    delays, simulated, theoretical = load_results()

    plt.figure(figsize=(9, 5.5))

    plt.plot(
        delays,
        simulated,
        marker="o",
        linewidth=2,
        label="Simulation Results"
    )

    plt.plot(
        delays,
        theoretical,
        marker="s",
        linestyle="--",
        linewidth=2,
        label="Theoretical Prediction"
    )

    plt.title(
        "Effect of Network Delay on Blockchain Fork Probability"
    )

    plt.xlabel("Network Delay (seconds)")
    plt.ylabel("Competing-Block Probability (%)")

    plt.xticks(delays)
    plt.ylim(bottom=0)

    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend()

    plt.tight_layout()

    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    png_file = output_dir / "fork_rate_graph.png"
    pdf_file = output_dir / "fork_rate_graph.pdf"

    plt.savefig(png_file, dpi=300)
    plt.savefig(pdf_file)

    print("=== CONSENSUS LAB: GRAPH RESULTS ===")
    print(f"PNG graph saved: {png_file}")
    print(f"PDF graph saved: {pdf_file}")

    plt.show()
    plt.close()


if __name__ == "__main__":
    create_graph()
