
# CONSENSUS LAB - WEEK 2, DAY 5
# Experiment 5: Proof-of-Work Chain Selection

import hashlib
import json


# STEP 1: Calculate a block's hash
def calculate_hash(block):
    block_data = {
        key: value
        for key, value in block.items()
        if key != "hash"
    }

    text = json.dumps(block_data, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# STEP 2: Mine a block
def mine_block(number, previous_hash, miner, difficulty=2):

    block = {
        "number": number,
        "previous_hash": previous_hash,
        "miner": miner,
        "difficulty": difficulty,
        "nonce": 0
    }

    target = "0" * difficulty

    while True:
        block_hash = calculate_hash(block)

        if block_hash.startswith(target):
            block["hash"] = block_hash
            return block

        block["nonce"] += 1


# STEP 3: Create a blockchain
def create_chain(miner, block_count):

    chain = []
    previous_hash = "GENESIS"

    for number in range(1, block_count + 1):

        block = mine_block(
            number,
            previous_hash,
            miner
        )

        chain.append(block)
        previous_hash = block["hash"]

    return chain


# STEP 4: Verify a blockchain
def validate_chain(chain):

    if not chain:
        return False

    expected_previous_hash = "GENESIS"

    for index, block in enumerate(chain):

        if block["number"] != index + 1:
            return False

        if block["previous_hash"] != expected_previous_hash:
            return False

        difficulty = block["difficulty"]

        if type(difficulty) is not int or not (1 <= difficulty <= 6):
            return False

        calculated_hash = calculate_hash(block)

        if calculated_hash != block["hash"]:
            return False

        if not calculated_hash.startswith("0" * difficulty):
            return False

        expected_previous_hash = block["hash"]

    return True


# STEP 5: Calculate accumulated work
def calculate_chain_work(chain):

    total_work = 0

    for block in chain:
        total_work += 16 ** block["difficulty"]

    return total_work


# STEP 6: Compare two chains
def select_chain(alice_chain, bob_chain):

    alice_valid = validate_chain(alice_chain)
    bob_valid = validate_chain(bob_chain)

    print("\n=== CHAIN VALIDATION ===")
    print("Alice's chain valid:", alice_valid)
    print("Bob's chain valid:", bob_valid)

    if not alice_valid and not bob_valid:
        return "Neither chain is valid"

    if alice_valid and not bob_valid:
        return "Alice"

    if bob_valid and not alice_valid:
        return "Bob"

    alice_work = calculate_chain_work(alice_chain)
    bob_work = calculate_chain_work(bob_chain)

    print("\n=== ACCUMULATED WORK ===")
    print("Alice's work:", alice_work)
    print("Bob's work:", bob_work)

    if alice_work > bob_work:
        return "Alice"

    if bob_work > alice_work:
        return "Bob"

    return "Tie - keep the current valid chain"


# STEP 7: Run the experiment
print("=== CONSENSUS LAB: CHAIN SELECTION ===")

alice_chain = create_chain("Alice", 3)
bob_chain = create_chain("Bob", 4)

print("\nAlice's blocks:", len(alice_chain))
print("Bob's blocks:", len(bob_chain))

winner = select_chain(alice_chain, bob_chain)

print("\n=== CONSENSUS RESULT ===")
print("Selected chain:", winner)

print("\nEXPERIMENT COMPLETE!")
