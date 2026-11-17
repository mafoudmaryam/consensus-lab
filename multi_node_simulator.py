
# CONSENSUS LAB - MULTI-NODE SIMULATOR
# Experiment 13: Five Miners with Network Delays

import csv
import heapq
import random
from pathlib import Path


NODE_NAMES = ["Alice", "Bob", "Charlie", "David", "Emma"]

SIMULATION_TIME = 100.0
AVERAGE_BLOCK_INTERVAL = 10.0
NETWORK_DELAY = 2.0
RANDOM_SEED = 42


class NetworkSimulator:
    def __init__(self):
        self.rng = random.Random(RANDOM_SEED)
        self.time = 0.0
        self.events = []
        self.counter = 0
        self.next_block_id = 0

        self.blocks = {
            "GENESIS": {
                "parent": None,
                "height": 0,
                "miner": "Network"
            }
        }

        self.tips = {
            name: "GENESIS" for name in NODE_NAMES
        }

        self.known_blocks = {
            name: {"GENESIS"} for name in NODE_NAMES
        }

        self.mined_blocks = 0
        self.competing_blocks = 0
        self.competing_pairs = set()

    def schedule(self, time, action, data):
        self.counter += 1

        heapq.heappush(
            self.events,
            (time, self.counter, action, data)
        )

    def schedule_mining(self, miner):
        # Each miner receives an equal share of mining power.
        rate = 1.0 / (
            AVERAGE_BLOCK_INTERVAL * len(NODE_NAMES)
        )

        wait = self.rng.expovariate(rate)
        next_time = self.time + wait

        if next_time <= SIMULATION_TIME:
            self.schedule(next_time, "mine", miner)

    def choose_tip(self, miner, block_id):
        current = self.tips[miner]

        new_height = self.blocks[block_id]["height"]
        old_height = self.blocks[current]["height"]

        if new_height > old_height:
            self.tips[miner] = block_id

        # Equal height: keep the current branch.

    def detect_competition(self, block_id):
        block = self.blocks[block_id]

        for other_id, other in self.blocks.items():
            if other_id == block_id or other_id == "GENESIS":
                continue

            if other["parent"] == block["parent"]:
                pair = tuple(sorted([block_id, other_id]))

                if pair not in self.competing_pairs:
                    self.competing_pairs.add(pair)
                    self.competing_blocks += 1

    def mine_block(self, miner):
        parent = self.tips[miner]

        self.next_block_id += 1
        block_id = f"B{self.next_block_id}"

        self.blocks[block_id] = {
            "parent": parent,
            "height": self.blocks[parent]["height"] + 1,
            "miner": miner
        }

        self.known_blocks[miner].add(block_id)
        self.tips[miner] = block_id
        self.mined_blocks += 1

        self.detect_competition(block_id)

        print(
            f"[{self.time:6.2f}s] "
            f"{miner} mines {block_id} "
            f"on {parent}"
        )

        # Broadcast to all other miners.
        for receiver in NODE_NAMES:
            if receiver != miner:
                self.schedule(
                    self.time + NETWORK_DELAY,
                    "receive",
                    (receiver, block_id)
                )

        self.schedule_mining(miner)

    def receive_block(self, receiver, block_id):
        self.known_blocks[receiver].add(block_id)

        self.choose_tip(receiver, block_id)

    def run(self):
        print("=== FIVE-NODE BLOCKCHAIN SIMULATION ===")

        for miner in NODE_NAMES:
            self.schedule_mining(miner)

        while self.events:
            time, _, action, data = heapq.heappop(self.events)
            self.time = time

            if action == "mine":
                self.mine_block(data)

            elif action == "receive":
                receiver, block_id = data
                self.receive_block(receiver, block_id)

        self.show_results()

    def show_results(self):
        fork_rate = (
            self.competing_blocks / self.mined_blocks * 100
            if self.mined_blocks else 0
        )

        final_tips = set(self.tips.values())
        final_agreement = len(final_tips) == 1

        print("\n=== FINAL RESULTS ===")
        print("Blocks mined:", self.mined_blocks)
        print("Competing pairs:", self.competing_blocks)
        print(f"Competing pairs per mined block: {fork_rate:.2f}%")
        print("Final agreement:", final_agreement)

        for miner, tip in self.tips.items():
            print(f"{miner}: {tip}")

        self.save_results(fork_rate, final_agreement)

    def save_results(self, fork_rate, agreement):
        output_dir = Path("results")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "multi_node_results.csv"

        with output_file.open("w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "nodes",
                "simulation_time_seconds",
                "network_delay_seconds",
                "blocks_mined",
                "competing_pairs",
                "competing_pairs_per_block_percent",
                "final_agreement"
            ])

            writer.writerow([
                len(NODE_NAMES),
                SIMULATION_TIME,
                NETWORK_DELAY,
                self.mined_blocks,
                self.competing_blocks,
                round(fork_rate, 2),
                agreement
            ])

        print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    simulator = NetworkSimulator()
    simulator.run()
