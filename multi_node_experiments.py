
# CONSENSUS LAB - FINAL NETWORK EXPERIMENTS
# Five-node blockchain simulation
# Repeated experiments with different network delays

import csv
import heapq
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


NODES = ["Alice", "Bob", "Charlie", "David", "Emma"]
DELAYS = [0.1, 0.5, 1.0, 3.0, 5.0]
REPETITIONS = 100
SIMULATION_TIME = 1000.0
AVERAGE_BLOCK_INTERVAL = 10.0
BASE_SEED = 2026

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


class BlockchainNetwork:
    def __init__(self, delay, seed):
        self.delay = delay
        self.rng = random.Random(seed)
        self.time = 0.0
        self.events = []
        self.event_number = 0
        self.block_number = 0

        self.blocks = {
            0: {"parent": None, "height": 0}
        }

        self.known = {n: {0} for n in NODES}
        self.tips = {n: 0 for n in NODES}
        self.pending = {n: set() for n in NODES}

    def schedule(self, time, action, data):
        self.event_number += 1
        heapq.heappush(
            self.events,
            (time, self.event_number, action, data)
        )

    def schedule_mining(self, node):
        # Total expected network mining interval: 10 seconds
        rate = 1 / (AVERAGE_BLOCK_INTERVAL * len(NODES))
        wait = self.rng.expovariate(rate)
        next_time = self.time + wait

        if next_time <= SIMULATION_TIME:
            self.schedule(next_time, "mine", node)

    def choose_tip(self, node, block_id):
        old = self.tips[node]
        new_height = self.blocks[block_id]["height"]
        old_height = self.blocks[old]["height"]

        # Deterministic tie-breaking:
        # higher chain first, then smaller block ID.
        if (
            new_height > old_height
            or (
                new_height == old_height
                and block_id < old
            )
        ):
            self.tips[node] = block_id

    def accept_block(self, node, block_id):
        if block_id in self.known[node]:
            return

        self.pending[node].add(block_id)

        # Process blocks only after their parents are known.
        changed = True

        while changed:
            changed = False

            for candidate in sorted(self.pending[node]):
                parent = self.blocks[candidate]["parent"]

                if parent in self.known[node]:
                    self.pending[node].remove(candidate)
                    self.known[node].add(candidate)
                    self.choose_tip(node, candidate)
                    changed = True
                    break

    def mine(self, node):
        parent = self.tips[node]

        self.block_number += 1
        block_id = self.block_number

        self.blocks[block_id] = {
            "parent": parent,
            "height": self.blocks[parent]["height"] + 1
        }

        self.known[node].add(block_id)
        self.choose_tip(node, block_id)

        # Broadcast to all other nodes.
        for receiver in NODES:
            if receiver != node:
                self.schedule(
                    self.time + self.delay,
                    "receive",
                    (receiver, block_id)
                )

        self.schedule_mining(node)

    def main_chain(self, tip):
        chain = set()
        current = tip

        while current is not None:
            chain.add(current)
            current = self.blocks[current]["parent"]

        return chain

    def run(self):
        for node in NODES:
            self.schedule_mining(node)

        # Process all mining and delivery events.
        # Mining stops at SIMULATION_TIME, but pending
        # deliveries continue afterward.
        while self.events:
            time, _, action, data = heapq.heappop(self.events)
            self.time = time

            if action == "mine":
                self.mine(data)
            else:
                node, block_id = data
                self.accept_block(node, block_id)

        final_tips = set(self.tips.values())
        agreement = len(final_tips) == 1

        # All nodes should know all blocks after delivery.
        all_delivered = all(
            len(self.known[node]) == len(self.blocks)
            for node in NODES
        )

        if not all_delivered:
            raise RuntimeError("Some blocks were not delivered")

        # Count blocks that share a parent with another block.
        parent_counts = Counter(
            block["parent"]
            for block_id, block in self.blocks.items()
            if block_id != 0
        )

        competing_blocks = sum(
            count
            for count in parent_counts.values()
            if count > 1
        )

        fork_events = sum(
            1 for count in parent_counts.values()
            if count > 1
        )

        # Deterministic chain selection should converge.
        if not agreement:
            raise RuntimeError("Nodes did not converge")

        tip = next(iter(final_tips))
        main_chain = self.main_chain(tip)

        stale_blocks = self.block_number - (
            len(main_chain) - 1
        )

        return {
            "delay": self.delay,
            "blocks_mined": self.block_number,
            "fork_events": fork_events,
            "competing_blocks": competing_blocks,
            "competing_block_percent": (
                100 * competing_blocks / self.block_number
                if self.block_number else 0
            ),
            "stale_block_percent": (
                100 * stale_blocks / self.block_number
                if self.block_number else 0
            ),
            "agreement": int(agreement)
        }


def main():
    all_rows = []
    summary = []

    print("=== FINAL MULTI-NODE EXPERIMENT ===")
    print(f"Nodes: {len(NODES)}")
    print(f"Repetitions per delay: {REPETITIONS}")
    print(f"Total simulations: {len(DELAYS) * REPETITIONS}")
    print()

    for delay_index, delay in enumerate(DELAYS):
        rows = []

        for repetition in range(REPETITIONS):
            seed = (
                BASE_SEED
                + delay_index * REPETITIONS
                + repetition
            )

            network = BlockchainNetwork(delay, seed)
            result = network.run()

            result["repetition"] = repetition + 1
            result["seed"] = seed

            rows.append(result)
            all_rows.append(result)

        mean_competing = statistics.mean(
            r["competing_block_percent"] for r in rows
        )

        mean_stale = statistics.mean(
            r["stale_block_percent"] for r in rows
        )

        mean_forks = statistics.mean(
            r["fork_events"] for r in rows
        )

        agreement_rate = statistics.mean(
            r["agreement"] for r in rows
        ) * 100

        summary.append({
            "delay_seconds": delay,
            "mean_competing_percent": round(mean_competing, 3),
            "mean_stale_percent": round(mean_stale, 3),
            "mean_fork_events": round(mean_forks, 3),
            "agreement_percent": round(agreement_rate, 2)
        })

        print(
            f"Delay {delay:>4.1f}s | "
            f"Competing: {mean_competing:>6.2f}% | "
            f"Stale: {mean_stale:>6.2f}% | "
            f"Agreement: {agreement_rate:.1f}%"
        )

    save_csv(
        RESULTS_DIR / "multi_node_all_runs.csv",
        all_rows
    )

    save_csv(
        RESULTS_DIR / "multi_node_summary.csv",
        summary
    )

    delays = [r["delay_seconds"] for r in summary]
    competing = [
        r["mean_competing_percent"] for r in summary
    ]
    stale = [
        r["mean_stale_percent"] for r in summary
    ]

    plt.figure(figsize=(9, 5.5))

    plt.plot(
        delays, competing,
        marker="o",
        label="Competing blocks"
    )

    plt.plot(
        delays, stale,
        marker="s",
        label="Stale blocks"
    )

    plt.xlabel("Network Delay (seconds)")
    plt.ylabel("Mean Percentage of Mined Blocks")
    plt.title("Impact of Network Delay on Blockchain Forks")
    plt.xticks(delays)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "multi_node_final_graph.png",
        dpi=300
    )

    plt.savefig(
        RESULTS_DIR / "multi_node_final_graph.pdf"
    )

    plt.close()

    print("\nFiles saved successfully!")
    print("FINAL NETWORK EXPERIMENT COMPLETE!")


def save_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
