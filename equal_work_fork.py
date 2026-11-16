
# CONSENSUS LAB - WEEK 2, DAY 6
# Experiment 6: Equal-Work Forks and Convergence

from chain_selection import (
    mine_block,
    validate_chain,
    calculate_chain_work
)


def show_chain(name, chain):
    print(f"\n{name}:")
    for block in chain:
        print(
            f"  Block {block['number']} | "
            f"Miner: {block['miner']} | "
            f"Hash: {block['hash'][:12]}..."
        )


def choose_chain(current_chain, candidate_chain):
    # Only compare valid blockchains.
    if not validate_chain(candidate_chain):
        return current_chain

    if not validate_chain(current_chain):
        return candidate_chain

    current_work = calculate_chain_work(current_chain)
    candidate_work = calculate_chain_work(candidate_chain)

    # Switch only if the candidate has more work.
    if candidate_work > current_work:
        return candidate_chain

    # On equal work, keep the current branch.
    return current_chain


def main():
    print("=== CONSENSUS LAB: EQUAL-WORK FORK ===")

    # Step 1: Mine two blocks shared by all nodes.
    genesis = mine_block(1, "GENESIS", "Network")
    second = mine_block(2, genesis["hash"], "Network")

    shared_history = [genesis, second]

    # Step 2: Alice and Bob mine competing third blocks.
    alice_block = mine_block(3, second["hash"], "Alice")
    bob_block = mine_block(3, second["hash"], "Bob")

    alice_chain = shared_history + [alice_block]
    bob_chain = shared_history + [bob_block]

    show_chain("Alice's chain", alice_chain)
    show_chain("Bob's chain", bob_chain)

    print("\n=== FORK DETECTED ===")
    print("Different third blocks:",
          alice_block["hash"] != bob_block["hash"])

    print("Alice's chain valid:", validate_chain(alice_chain))
    print("Bob's chain valid:", validate_chain(bob_chain))

    print("Alice's work:", calculate_chain_work(alice_chain))
    print("Bob's work:", calculate_chain_work(bob_chain))

    # Step 3: Each node initially follows its own chain.
    alice_view = alice_chain
    bob_view = bob_chain

    # The nodes receive each other's competing chain.
    alice_view = choose_chain(alice_view, bob_chain)
    bob_view = choose_chain(bob_view, alice_chain)

    print("\n=== EQUAL-WORK DECISION ===")
    print("Alice keeps her branch:",
          alice_view[-1]["hash"] == alice_block["hash"])
    print("Bob keeps his branch:",
          bob_view[-1]["hash"] == bob_block["hash"])

    print("Nodes agree:",
          alice_view[-1]["hash"] == bob_view[-1]["hash"])

    # Step 4: Alice mines one more block.
    alice_fourth = mine_block(
        4,
        alice_block["hash"],
        "Alice"
    )

    longer_alice_chain = alice_chain + [alice_fourth]

    print("\n=== ALICE MINES ANOTHER BLOCK ===")
    print("Alice's new work:",
          calculate_chain_work(longer_alice_chain))
    print("Bob's old work:",
          calculate_chain_work(bob_view))

    # Step 5: Both nodes receive Alice's new chain.
    alice_view = choose_chain(alice_view, longer_alice_chain)
    bob_view = choose_chain(bob_view, longer_alice_chain)

    print("\n=== FINAL CONSENSUS ===")
    print("Alice's selected tip:",
          alice_view[-1]["hash"][:12])
    print("Bob's selected tip:",
          bob_view[-1]["hash"][:12])

    print("Nodes agree:",
          alice_view[-1]["hash"] == bob_view[-1]["hash"])

    print("\nEXPERIMENT COMPLETE!")


if __name__ == "__main__":
    main()
