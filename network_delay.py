
# CONSENSUS LAB - WEEK 3, DAY 1
# Experiment 7: Network Delay Simulation

import heapq


class NetworkSimulator:
    def __init__(self):
        self.current_time = 0.0
        self.events = []
        self.event_counter = 0

        self.nodes = {
            "Alice": set(),
            "Bob": set(),
            "Charlie": set()
        }

        self.received_at = {}

    def schedule_delivery(self, sender, receiver, block_id, delay):
        if delay < 0:
            raise ValueError("Network delay cannot be negative")

        delivery_time = self.current_time + delay

        self.event_counter += 1

        heapq.heappush(
            self.events,
            (
                delivery_time,
                self.event_counter,
                sender,
                receiver,
                block_id
            )
        )

        print(
            f"[t={self.current_time:.1f}s] "
            f"{sender} sends {block_id} to {receiver}. "
            f"Delay: {delay:.1f}s"
        )

    def create_block(self, miner, block_id):
        self.nodes[miner].add(block_id)
        self.received_at[(miner, block_id)] = self.current_time

        print(
            f"[t={self.current_time:.1f}s] "
            f"{miner} creates {block_id}"
        )

    def run(self):
        while self.events:
            (
                delivery_time,
                _,
                sender,
                receiver,
                block_id
            ) = heapq.heappop(self.events)

            self.current_time = delivery_time

            if block_id not in self.nodes[receiver]:
                self.nodes[receiver].add(block_id)
                self.received_at[(receiver, block_id)] = self.current_time

                print(
                    f"[t={self.current_time:.1f}s] "
                    f"{receiver} receives {block_id} from {sender}"
                )

    def show_results(self, block_id):
        print("\n=== EXPERIMENT RESULTS ===")

        for node in self.nodes:
            received_time = self.received_at.get(
                (node, block_id)
            )

            if received_time is None:
                print(f"{node}: Did not receive the block")
            else:
                print(
                    f"{node}: Learned about {block_id} "
                    f"at {received_time:.1f}s"
                )

        if all(block_id in blocks for blocks in self.nodes.values()):
            convergence_time = max(
                self.received_at[(node, block_id)]
                for node in self.nodes
            )

            print("\nAll nodes received the block: True")
            print(f"Knowledge convergence time: {convergence_time:.1f}s")
        else:
            print("\nAll nodes received the block: False")


def main():
    print("=== CONSENSUS LAB: NETWORK DELAY ===")

    simulator = NetworkSimulator()

    simulator.create_block("Alice", "Block-3A")

    simulator.schedule_delivery(
        "Alice", "Bob", "Block-3A", delay=2
    )

    simulator.schedule_delivery(
        "Alice", "Charlie", "Block-3A", delay=5
    )

    simulator.run()
    simulator.show_results("Block-3A")

    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
