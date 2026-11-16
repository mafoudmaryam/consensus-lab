
import hashlib
import json

# Step 1: Create our first block
block = {
    "number": 1,
"transaction": "Alice sends Bob 9 coins",
    "previous_hash": "0000"
}

# Step 2: Convert the block into consistent text
block_text = json.dumps(block, sort_keys=True)

# Step 3: Calculate the SHA-256 hash
block_hash = hashlib.sha256(
    block_text.encode("utf-8")
).hexdigest()

# Step 4: Show the result
print("=== MY FIRST BLOCK ===")
print("Block number:", block["number"])
print("Transaction:", block["transaction"])
print("Previous hash:", block["previous_hash"])
print("Block hash:", block_hash)
