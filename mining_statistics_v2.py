
# CONSENSUS LAB - WEEK 2, DAY 4
# Experiment 4: Improved Mining Statistics

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
        "trial_id": f"d{difficulty}-t{trial}",
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


# STEP 3: Experiment settings
difficulties = [2, 3, 4]
trials_per_difficulty = 30

results = []
summary = []

print("=== IMPROVED MINING STATISTICS ===")
print("Trials per difficulty:", trials_per_difficulty)


# STEP 4: Run experiments
for difficulty in difficulties:

    print(f"\n=== DIFFICULTY {difficulty} ===")

    group = []

    for trial in range(1, trials_per_difficulty + 1):

        result = mine_block(difficulty, trial)

        results.append(result)
        group.append(result)

        print(
            f"Trial {trial:2d} | "
            f"Attempts: {result['attempts']:8d} | "
            f"Time: {result['time_seconds']:.6f}s | "
            f"Valid: {result['verified']}"
        )

    # STEP 5: Calculate statistics
    attempts = [r["attempts"] for r in group]
    times = [r["time_seconds"] for r in group]

    row = {
        "difficulty": difficulty,
        "trials": len(group),
        "mean_attempts": statistics.mean(attempts),
        "median_attempts": statistics.median(attempts),
        "min_attempts": min(attempts),
        "max_attempts": max(attempts),
        "std_attempts": statistics.stdev(attempts),
        "mean_time_seconds": statistics.mean(times),
        "median_time_seconds": statistics.median(times)
    }

    summary.append(row)


# STEP 6: Print summary
print("\n=== FINAL STATISTICAL SUMMARY ===")

for row in summary:

    print(f"\nDifficulty: {row['difficulty']}")
    print("Trials:", row["trials"])
    print("Mean attempts:", round(row["mean_attempts"], 2))
    print("Median attempts:", row["median_attempts"])
    print("Minimum attempts:", row["min_attempts"])
    print("Maximum attempts:", row["max_attempts"])
    print("Standard deviation:", round(row["std_attempts"], 2))
    print(
        "Mean mining time:",
        round(row["mean_time_seconds"], 6),
        "seconds"
    )


# STEP 7: Create results folder
output_folder = Path("results")
output_folder.mkdir(exist_ok=True)


# STEP 8: Save detailed trial results
details_file = output_folder / "mining_statistics_v2.csv"

with open(details_file, "w", newline="", encoding="utf-8") as file:

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


# STEP 9: Save statistical summary
summary_file = output_folder / "mining_summary_v2.csv"

with open(summary_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "difficulty",
            "trials",
            "mean_attempts",
            "median_attempts",
            "min_attempts",
            "max_attempts",
            "std_attempts",
            "mean_time_seconds",
            "median_time_seconds"
        ]
    )

    writer.writeheader()
    writer.writerows(summary)


# STEP 10: Final checks
print("\n=== EXPERIMENT CHECK ===")
print("Total trials:", len(results))
print("All results valid:", all(r["verified"] for r in results))
print("Detailed results:", details_file)
print("Statistical summary:", summary_file)

print("\nEXPERIMENT COMPLETE!")
