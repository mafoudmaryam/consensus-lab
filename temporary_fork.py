
# CONSENSUS LAB - DAY 7
# Experiment 3: Creating a temporary fork

import copy
import hashlib
import json


# STEP 1: Calculate a block's hash
def calculate_hash(block):
    block_text = json.dumps(block, sort_keys=True)
    return hashlib.sha256(
        block_text.encode("utf-8")
    ).hexdigest()


# STEP 2: Create the shared blockchain
block1 = {
    "number": 1,
    "data": "Alice sends Bob 3 coins",
    "previous_hash": "0000"
}

block2 = {
    "number": 2,
    "data": "Bob sends Emma 2 coins",
    "previous_hash": calculate_hash(block1)
}

shared_blockchain = [block1, block2]


# STEP 3: Create independent node copies
alice_chain = copy.deepcopy(shared_blockchain)
bob_chain = copy.deepcopy(shared_blockchain)


# STEP 4: Alice receives Block 3A
block3a = {
    "number": 3,
    "data": "Emma sends Alice 1 coin",
    "previous_hash": calculate_hash(block2)
}

alice_chain.append(block3a)


# STEP 5: Bob receives a different Block 3B
block3b = {
    "number": 3,
    "data": "Alice sends Bob 2 coins",
    "previous_hash": calculate_hash(block2)
}

bob_chain.append(block3b)


# STEP 6: Display both blockchains
print("=== ALICE'S BLOCKCHAIN ===")

for block in alice_chain:
    print("Block:", block["number"])
    print("Data:", block["data"])
    print("Hash:", calculate_hash(block))
    print("------------------------")


print("\n=== BOB'S BLOCKCHAIN ===")

for block in bob_chain:
    print("Block:", block["number"])
    print("Data:", block["data"])
    print("Hash:", calculate_hash(block))
    print("------------------------")


# STEP 7: Compare the chains
print("\n=== CHECKING AGREEMENT ===")

if alice_chain == bob_chain:
    print("The nodes agree!")
else:
    print("FORK DETECTED!")
    print("Alice and Bob have different blockchains.")


# STEP 8: Compare their third blocks
print("\n=== COMPARING BLOCK 3 ===")

print("Alice's Block 3 hash:", calculate_hash(block3a))
print("Bob's Block 3 hash:", calculate_hash(block3b))

print(
    "Same previous hash?",
    block3a["previous_hash"] == block3b["previous_hash"]
)

print(
    "Same block hash?",
    calculate_hash(block3a) == calculate_hash(block3b)
)
