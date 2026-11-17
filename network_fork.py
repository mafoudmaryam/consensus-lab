
# CONSENSUS LAB - WEEK 3, DAY 2
# Experiment 8: Network Delays and Temporary Forks

import heapq

from chain_selection import (
    mine_block,
    validate_chain,
    calculate_chain_work
)


class ForkSimulator:
    def __init__(self):
        self.current_time = 0
        self.events = []
        self.counter = 0

        self.views = {
            "Alice": [],
            "Bob": []
        }

        self.fork_detected = False
        self.fork_start = None
        self.convergence_time = None

    def schedule(self, time, action, data=None):
        self.counter += 1
        heapq.heappush(
            self.events,
            (time, self.counter, action, data)
        )

    def choose_chain(self, current, candidate):
        if not validate_chain(candidate):
            return current

        if not validate_chain(current):
            return candidate

        if calculate_chain_work(candidate) > calculate_chain_work(current):
            return candidate

        # Equal work: keep current branch
        return current

    def mine(self, miner):
        current_chain = self.views[miner]
        previous = current_chain[-1]

        new_block = mine_block(
            previous["number"] + 1,
            previous["hash"],
            miner,
            difficulty=2
        )

        new_chain = current_chain + [new_block]
        self.views[miner] = new_chain

        print(
            f"[t={self.current_time}s] "
            f"{miner} mines Block {new_block['number']} "
            f"({new_block['hash'][:10]}...)"
        )

        return new_chain

    def receive_chain(self, receiver, chain):
        old_chain = self.views[receiver]
        new_chain = self.choose_chain(old_chain, chain)

        self.views[receiver] = new_chain

        changed = new_chain[-1]["hash"] != old_chain[-1]["hash"]

        print(
            f"[t={self.current_time}s] "
            f"{receiver} receives a competing chain. "
            f"Switched: {changed}"
        )

    def check_consensus(self):
        alice_tip = self.views["Alice"][-1]["hash"]
        bob_tip = self.views["Bob"][-1]["hash"]

        agree = alice_tip == bob_tip

        if not agree and not self.fork_detected:
            self.fork_detected = True
            self.fork_start = self.current_time

            print(
                f"[t={self.current_time}s] "
                "TEMPORARY DISAGREEMENT DETECTED"
            )

        if agree and self.fork_start is not None:
            if self.convergence_time is None:
                self.convergence_time = self.current_time

                print(
                    f"[t={self.current_time}s] "
                    "NODES CONVERGED"
                )

    def run(self):
        while self.events:
            time, _, action, data = heapq.heappop(self.events)
            self.current_time = time

            if action == "mine":
                self.mine(data)

            elif action == "receive":
                receiver, chain = data
                self.receive_chain(receiver, chain)

            self.check_consensus()


def main():
    print("=== CONSENSUS LAB: NETWORK FORK ===")

    sim = ForkSimulator()

    # Shared blockchain history
    genesis = mine_block(1, "GENESIS", "Network")
    second = mine_block(2, genesis["hash"], "Network")

    shared = [genesis, second]

    sim.views["Alice"] = shared.copy()
    sim.views["Bob"] = shared.copy()

    # Alice mines Block 3A at t=0
    sim.schedule(0, "mine", "Alice")

    # Bob mines Block 3B at t=3
    sim.schedule(3, "mine", "Bob")

    # Alice's Block 3A reaches Bob at t=5
    # Capture the chain after Alice mines.
    sim.run_until = None

    # Process Alice's first mining event
    time, _, action, data = heapq.heappop(sim.events)
    sim.current_time = time
    alice_chain = sim.mine(data)
    sim.check_consensus()

    # Schedule Alice's chain delivery to Bob
    sim.schedule(5, "receive", ("Bob", alice_chain.copy()))

    # Alice mines Block 4A at t=8
    sim.schedule(8, "mine", "Alice")

    # Process events until t=8
    while sim.events and sim.events[0][0] <= 8:
        time, _, action, data = heapq.heappop(sim.events)
        sim.current_time = time

        if action == "mine":
            sim.mine(data)
        elif action == "receive":
            receiver, chain = data
            sim.receive_chain(receiver, chain)

        sim.check_consensus()

    # Alice's stronger chain reaches Bob at t=10
    stronger_alice_chain = sim.views["Alice"].copy()

    sim.schedule(
        10,
        "receive",
        ("Bob", stronger_alice_chain)
    )

    sim.run()

    print("\n=== EXPERIMENT RESULTS ===")
    print("Fork/disagreement detected:", sim.fork_detected)

    if sim.fork_start is not None:
        print("Disagreement started at:", sim.fork_start, "seconds")

    if sim.convergence_time is not None:
        print("Nodes converged at:", sim.convergence_time, "seconds")
        print(
            "Disagreement duration:",
            sim.convergence_time - sim.fork_start,
            "seconds"
        )

    alice_tip = sim.views["Alice"][-1]["hash"]
    bob_tip = sim.views["Bob"][-1]["hash"]

    print("Final consensus:", alice_tip == bob_tip)
    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
