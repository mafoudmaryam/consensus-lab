
import hashlib
import json


# STEP 1: Calculate the SHA-256 hash of a block
def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True)
    return hashlib.sha256(
        block_string.encode("utf-8")
    ).hexdigest()


# STEP 2: Create Block 1
block1 = {
    "number": 1,
    "transaction": "Alice sends Bob 3 coins",
    "previous_hash": "0000"
}

hash1 = calculate_hash(block1)


# STEP 3: Create Block 2
block2 = {
    "number": 2,
    "transaction": "Bob sends Emma 2 coins",
    "previous_hash": hash1
}

hash2 = calculate_hash(block2)


# STEP 4: Create Block 3
block3 = {
    "number": 3,
    "transaction": "Emma sends Alice 1 coin",
    "previous_hash": hash2
}

hash3 = calculate_hash(block3)


# STEP 5: Put all blocks into a Python list
blockchain = [block1, block2, block3]


# STEP 6: Automatically validate block connections
def validate_blockchain(blockchain):

    for i in range(1, len(blockchain)):

        previous_block = blockchain[i - 1]
        current_block = blockchain[i]

        expected_hash = calculate_hash(previous_block)

        if current_block["previous_hash"] != expected_hash:
            print(
                "Broken connection at Block",
                current_block["number"]
            )
            return False

    print("All block connections are valid!")
    return True


# STEP 7: Display the original blockchain
print("=== ORIGINAL BLOCKCHAIN ===")

for block in blockchain:
    print("Block number:", block["number"])
    print("Transaction:", block["transaction"])
    print("Previous hash:", block["previous_hash"])
    print("Current hash:", calculate_hash(block))
    print("------------------------")


# STEP 8: Validate before tampering
print("\n=== BEFORE TAMPERING ===")
validate_blockchain(blockchain)



# STEP 9: Tamper with Block 3
print("\n=== TAMPERING WITH BLOCK 3 ===")

print("Original transaction:", block3["transaction"])
print("Original Block 3 hash:", hash3)

block3["transaction"] = "Emma sends Alice 100 coins"

new_hash3 = calculate_hash(block3)

print("Modified transaction:", block3["transaction"])
print("New Block 3 hash:", new_hash3)

print("Did Block 3's hash change?", hash3 != new_hash3)

# Compare Block 3 with its saved original hash
if new_hash3 != hash3:
    print("WARNING: Block 3 has been modified!")
else:
    print("Block 3 matches its original hash.")



# STEP 10: Validate after tampering
print("\n=== AFTER TAMPERING ===")
validate_blockchain(blockchain)
