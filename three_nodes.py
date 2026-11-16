
# CONSENSUS LAB - DAY 7
# Experiment 2: Sharing a new block between nodes

import copy

# STEP 1: Starting blockchain
original_blockchain = [
    {"number": 1, "data": "Alice sends Bob 3 coins"},
    {"number": 2, "data": "Bob sends Emma 2 coins"}
]

# STEP 2: Create three independent nodes
nodes = {
    "Alice": copy.deepcopy(original_blockchain),
    "Bob": copy.deepcopy(original_blockchain),
    "Emma": copy.deepcopy(original_blockchain)
}

# STEP 3: Alice receives Block 3
new_block = {
    "number": 3,
    "data": "Emma sends Alice 1 coin"
}

nodes["Alice"].append(copy.deepcopy(new_block))

print("=== BEFORE SHARING ===")

for name, blockchain in nodes.items():
    print(name, "has", len(blockchain), "blocks")

# STEP 4: Alice shares Block 3 with Bob and Emma
print("\n=== SHARING BLOCK 3 ===")

nodes["Bob"].append(copy.deepcopy(new_block))
print("Bob received Block 3!")

nodes["Emma"].append(copy.deepcopy(new_block))
print("Emma received Block 3!")

# STEP 5: Display updated blockchains
print("\n=== AFTER SHARING ===")

for name, blockchain in nodes.items():
    print(name, "has", len(blockchain), "blocks")

# STEP 6: Check whether all nodes agree
print("\n=== DO ALL NODES AGREE? ===")

if nodes["Alice"] == nodes["Bob"] == nodes["Emma"]:
    print("YES! All nodes have the same blockchain.")
else:
    print("NO! Nodes still have different blockchains.")
