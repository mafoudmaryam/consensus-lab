
# CONSENSUS LAB - WEEK 3, DAY 3
# Experiment 9: Accurate Fork Detection

import csv
import heapq
from pathlib import Path

from chain_selection import (
    mine_block,
    validate_chain,
    calculate_chain_work
)


class ForkSimulator:
    def __init__(self):
        self.time = 0
        self.events = []
        self.counter = 0

        self.chains = {}
        self.all_blocks = {}

        self.fork_time = None
        self.resolution_time = None
        self.fork_parent = None

    def schedule(self, time, action, data):
        self.counter += 1
        heapq.heappush(
            self.events,
            (time, self.counter, action, data)
        )

    def remember_block(self, block):
        # Record every block, including competing blocks.
        block_hash = block["hash"]
        self.all_blocks[block_hash] = block

        # Detect two different blocks at the same height
        # that share the same parent.
        for other_hash, other in self.all_blocks.items():
            if other_hash == block_hash:
                continue

            same_height = other["number"] == block["number"]
            same_parent = (
                other["previous_hash"] == block["previous_hash"]
            )

            if same_height and same_parent:
                if self.fork_time is None:
                    self.fork_time = self.time
                    self.fork_parent = block["previous_hash"]

                    print(
                        f"[t={self.time}s] "
                        "REAL FORK DETECTED!"
                    )

    def mine(self, miner):
        chain = self.chains[miner]
        previous = chain[-1]

        block = mine_block(
            previous["number"] + 1,
            previous["hash"],
            miner,
            difficulty=2
        )

        self.chains[miner] = chain + [block]
        self.remember_block(block)

        print(
            f"[t={self.time}s] "
            f"{miner} mines Block {block['number']}"
        )

    def receive(self, receiver, candidate):
        current = self.chains[receiver]

        if not validate_chain(candidate):
            print("Rejected invalid chain")
            return

        if calculate_chain_work(candidate) > calculate_chain_work(current):
            self.chains[receiver] = candidate.copy()
            print(
                f"[t={self.time}s] "
                f"{receiver} switches to stronger chain"
            )
        else:
            print(
                f"[t={self.time}s] "
                f"{receiver} keeps current chain"
            )

    def check_resolution(self):
        if self.fork_time is None:
            return

        if self.resolution_time is not None:
            return

        alice_tip = self.chains["Alice"][-1]["hash"]
        bob_tip = self.chains["Bob"][-1]["hash"]

        if alice_tip == bob_tip:
            self.resolution_time = self.time
            print(
                f"[t={self.time}s] "
                "FORK RESOLVED: nodes agree"
            )

    def process_next(self):
        time, _, action, data = heapq.heappop(self.events)
        self.time = time

        if action == "mine":
            self.mine(data)

        elif action == "receive":
            receiver, chain = data
            self.receive(receiver, chain)

        self.check_resolution()

    def run_until(self, end_time):
        while self.events and self.events[0][0] <= end_time:
            self.process_next()

    def run(self):
        while self.events:
            self.process_next()


def save_results(sim):
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "network_fork_v2.csv"

    lifetime = None
    if (
        sim.fork_time is not None
        and sim.resolution_time is not None
    ):
        lifetime = sim.resolution_time - sim.fork_time

    final_agreement = (
        sim.chains["Alice"][-1]["hash"]
        == sim.chains["Bob"][-1]["hash"]
    )

    with output_file.open("w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "experiment",
            "fork_detected",
            "fork_time_seconds",
            "resolution_time_seconds",
            "fork_lifetime_seconds",
            "final_agreement"
        ])

        writer.writerow([
            "network_fork_v2",
            sim.fork_time is not None,
            sim.fork_time,
            sim.resolution_time,
            lifetime,
            final_agreement
        ])

    print(f"\nResults saved to: {output_file}")


def main():
    print("=== CONSENSUS LAB: ACCURATE FORK DETECTION ===")

    sim = ForkSimulator()

    genesis = mine_block(1, "GENESIS", "Network")
    second = mine_block(2, genesis["hash"], "Network")

    shared = [genesis, second]

    sim.chains["Alice"] = shared.copy()
    sim.chains["Bob"] = shared.copy()

    sim.remember_block(genesis)
    sim.remember_block(second)

    # Alice creates Block 3A at time 0
    sim.schedule(0, "mine", "Alice")
    sim.run_until(0)

    alice_block_3 = sim.chains["Alice"].copy()

    # Bob creates competing Block 3B at time 3
    sim.schedule(3, "mine", "Bob")

    # Alice's Block 3A arrives at Bob at time 5
    sim.schedule(5, "receive", ("Bob", alice_block_3))

    # Alice creates Block 4A at time 8
    sim.schedule(8, "mine", "Alice")
    sim.run_until(8)

    # Stronger chain reaches Bob at time 10
    alice_stronger_chain = sim.chains["Alice"].copy()

    sim.schedule(
        10,
        "receive",
        ("Bob", alice_stronger_chain)
    )

    sim.run()

    lifetime = None
    if (
        sim.fork_time is not None
        and sim.resolution_time is not None
    ):
        lifetime = sim.resolution_time - sim.fork_time

    print("\n=== EXPERIMENT RESULTS ===")
    print("Fork detected:", sim.fork_time is not None)
    print("Fork formation time:", sim.fork_time)
    print("Fork resolution time:", sim.resolution_time)
    print("Fork lifetime:", lifetime)

    final_agreement = (
        sim.chains["Alice"][-1]["hash"]
        == sim.chains["Bob"][-1]["hash"]
    )
    print("Final agreement:", final_agreement)

    save_results(sim)

    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
