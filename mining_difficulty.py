
# CONSENSUS LAB - WEEK 2, DAY 2
# Experiment: How mining difficulty affects performance

import hashlib
import json
import time
import copy


# STEP 1: Calculate the hash of a block
def calculate_hash(block):
    block_text = json.dumps(block, sort_keys=True)
    return hashlib.sha256(
        block_text.encode("utf-8")
    ).hexdigest()


# STEP 2: Mine a block at a chosen difficulty
def mine_block(original_block, difficulty):

    block = copy.deepcopy(original_block)
    block["nonce"] = 0

    target = "0" * difficulty
    attempts = 0

    start_time = time.perf_counter()

    while True:
        attempts += 1

        block_hash = calculate_hash(block)

        if block_hash.startswith(target):
            break

        block["nonce"] += 1

    end_time = time.perf_counter()

    mining_time = end_time - start_time

    return {
        "difficulty": difficulty,
        "nonce": block["nonce"],
        "attempts": attempts,
        "time": mining_time,
        "hash": block_hash
    }


# STEP 3: Create our original block
original_block = {
    "number": 1,
    "transactions": [
        {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 3
        }
    ],
    "previous_hash": "0000",
    "nonce": 0
}


# STEP 4: Test three difficulty levels
difficulties = [2, 3, 4]

results = []

print("=== MINING DIFFICULTY EXPERIMENT ===")

for difficulty in difficulties:

    print("\nMining with difficulty:", difficulty)

    result = mine_block(original_block, difficulty)

    results.append(result)

    print("Winning nonce:", result["nonce"])
    print("Total attempts:", result["attempts"])
    print("Mining time:", round(result["time"], 6), "seconds")
    print("Winning hash:", result["hash"])


# STEP 5: Display a comparison
print("\n=== FINAL COMPARISON ===")

print(
    f"{'Difficulty':<12}"
    f"{'Attempts':<12}"
    f"{'Time (seconds)':<18}"
)

print("-" * 42)

for result in results:
    print(
        f"{result['difficulty']:<12}"
        f"{result['attempts']:<12}"
        f"{result['time']:<18.6f}"
    )


# STEP 6: Check each result
print("\n=== VERIFYING RESULTS ===")

for result in results:

    target = "0" * result["difficulty"]

    if result["hash"].startswith(target):
        print(
            "Difficulty",
            result["difficulty"],
            ": VALID"
        )
    else:
        print(
            "Difficulty",
            result["difficulty"],
            ": INVALID"
        )


print("\nEXPERIMENT COMPLETE!")
