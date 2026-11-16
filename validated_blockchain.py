
# CONSENSUS LAB - DAY 6
# Connecting validated blocks into a blockchain

import hashlib
import json

from transaction_validator import validate_transaction


# STEP 1: Starting balances
balances = {
    "Alice": 10,
    "Bob": 5,
    "Emma": 2
}

blockchain = []


# STEP 2: Function to calculate a block's hash
def calculate_hash(block):
    block_text = json.dumps(block, sort_keys=True)
    block_bytes = block_text.encode("utf-8")
    return hashlib.sha256(block_bytes).hexdigest()


# STEP 3: Function to validate and add a block
def add_block(block, balances, blockchain):

    print("\n=== CHECKING BLOCK", block["number"], "===")

    # Check the connection to the previous block
    if len(blockchain) == 0:
        expected_previous_hash = "0000"
    else:
        expected_previous_hash = calculate_hash(blockchain[-1])

    if block["previous_hash"] != expected_previous_hash:
        print("BLOCK REJECTED: Wrong previous hash!")
        return False

    # Check transactions using temporary balances
    temporary_balances = balances.copy()

    for transaction in block["transactions"]:

        print("Checking transaction:", transaction)

        if not validate_transaction(transaction, temporary_balances):
            print("BLOCK REJECTED: Invalid transaction!")
            return False

        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]

        temporary_balances[sender] -= amount
        temporary_balances[receiver] += amount

    # Commit changes only after all checks pass
    balances.update(temporary_balances)
    blockchain.append(block)

    print("BLOCK ACCEPTED!")
    print("Balances:", balances)
    print("Block hash:", calculate_hash(block))

    return True


# STEP 4: Create Block 1
block1 = {
    "number": 1,
    "transactions": [
        {"sender": "Alice", "receiver": "Bob", "amount": 3},
        {"sender": "Bob", "receiver": "Emma", "amount": 2}
    ],
    "previous_hash": "0000"
}

add_block(block1, balances, blockchain)


# STEP 5: Create Block 2
block2 = {
    "number": 2,
    "transactions": [
        {"sender": "Emma", "receiver": "Alice", "amount": 1}
    ],
    "previous_hash": calculate_hash(block1)
}

add_block(block2, balances, blockchain)


# STEP 6: Display the blockchain
print("\n=== FINAL BLOCKCHAIN ===")

for block in blockchain:
    print("Block number:", block["number"])
    print("Previous hash:", block["previous_hash"])
    print("Block hash:", calculate_hash(block))
    print("------------------------")


# STEP 7: Display final balances
print("\n=== FINAL BALANCES ===")
print(balances)
