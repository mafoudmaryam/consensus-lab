
# CONSENSUS LAB - WEEK 2, DAY 1
# My first Proof-of-Work mining experiment

import hashlib
import json
import time


# STEP 1: Create a block
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
    "nonce": 0
}


# STEP 2: Set mining difficulty
difficulty = 3
target = "0" * difficulty


# STEP 3: Function to calculate the block hash
def calculate_hash(block):
    block_text = json.dumps(block, sort_keys=True)
    block_bytes = block_text.encode("utf-8")

    return hashlib.sha256(block_bytes).hexdigest()


# STEP 4: Start mining
print("=== STARTING MINING ===")
print("Difficulty:", difficulty)
print("Required hash prefix:", target)

start_time = time.time()
attempts = 0


# STEP 5: Keep trying different nonces
while True:

    attempts += 1

    block_hash = calculate_hash(block)

    if block_hash.startswith(target):
        print("\nMINING SUCCESSFUL!")
        break

    block["nonce"] += 1


# STEP 6: Calculate mining time
end_time = time.time()
mining_time = end_time - start_time


# STEP 7: Display results
print("\n=== MINING RESULTS ===")
print("Block number:", block["number"])
print("Winning nonce:", block["nonce"])
print("Block hash:", block_hash)
print("Total attempts:", attempts)
print("Mining time:", round(mining_time, 4), "seconds")


# STEP 8: Verify the mined block
print("\n=== VERIFYING BLOCK ===")

verification_hash = calculate_hash(block)

if verification_hash.startswith(target):
    print("Proof-of-Work is VALID!")
else:
    print("Proof-of-Work is INVALID!")
