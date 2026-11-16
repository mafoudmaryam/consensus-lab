
# CONSENSUS LAB - WEEK 2, DAY 3
# Experiment 3: Repeated mining and statistics

import hashlib
import json
import time
import csv
import statistics
from pathlib import Path


# STEP 1: Calculate SHA-256 hash
def calculate_hash(block):
    block_text = json.dumps(block, sort_keys=True)
    block_bytes = block_text.encode("utf-8")

    return hashlib.sha256(block_bytes).hexdigest()


# STEP 2: Mine one block
def mine_block(difficulty, trial):

    block = {
        "number": 1,
        "transactions": [
            {
                "sender": "Alice",
                "receiver": "Bob",
                "amount": 3
            }
        ],
        "previous_hash": "0000",
        "trial_id": trial,
        "nonce": 0
    }

    target = "0" * difficulty
    attempts = 0

    start_time = time.perf_counter()

    while True:
        attempts += 1

        block_hash = calculate_hash(block)

        if block_hash.startswith(target):
            break

        block["nonce"] += 1

    mining_time = time.perf_counter() - start_time

    # Check the result
    verified = (
        calculate_hash(block) == block_hash
        and block_hash.startswith(target)
    )

    return {
        "difficulty": difficulty,
        "trial": trial,
        "nonce": block["nonce"],
        "attempts": attempts,
        "time_seconds": mining_time,
        "hash": block_hash,
        "verified": verified
    }


# STEP 3: Choose experiment settings
difficulties = [2, 3, 4]
trials_per_difficulty = 10

results = []

print("=== MINING STATISTICS EXPERIMENT ===")
print("Trials per difficulty:", trials_per_difficulty)


# STEP 4: Run all mining trials
for difficulty in difficulties:

    print("\n=== DIFFICULTY", difficulty, "===")

    for trial in range(1, trials_per_difficulty + 1):

        result = mine_block(difficulty, trial)

        results.append(result)

        print(
            f"Trial {trial:2d} | "
            f"Attempts: {result['attempts']:7d} | "
            f"Time: {result['time_seconds']:.6f}s | "
            f"Valid: {result['verified']}"
        )


# STEP 5: Calculate statistics
print("\n=== FINAL STATISTICS ===")

for difficulty in difficulties:

    group = [
        result for result in results
        if result["difficulty"] == difficulty
    ]

    attempts = [r["attempts"] for r in group]
    times = [r["time_seconds"] for r in group]

    average_attempts = statistics.mean(attempts)
    average_time = statistics.mean(times)

    print("\nDifficulty:", difficulty)
    print("Number of trials:", len(group))
    print("Average attempts:", round(average_attempts, 2))
    print("Minimum attempts:", min(attempts))
    print("Maximum attempts:", max(attempts))
    print("Average mining time:", round(average_time, 6), "seconds")


# STEP 6: Save results to a CSV file
output_folder = Path("results")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "mining_statistics.csv"

with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "difficulty",
            "trial",
            "nonce",
            "attempts",
            "time_seconds",
            "hash",
            "verified"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


# STEP 7: Final checks
print("\n=== EXPERIMENT CHECK ===")
print("Total trials:", len(results))
print("All results valid:", all(r["verified"] for r in results))
print("Results saved to:", output_file)

print("\nEXPERIMENT COMPLETE!")
