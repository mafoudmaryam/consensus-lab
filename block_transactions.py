
# CONSENSUS LAB - DAY 5
# Validating transactions inside a block

import hashlib
import json
from transaction_validator import validate_transaction

# STEP 1: Starting balances
balances = {
    "Alice": 10,
    "Bob": 5,
    "Emma": 2
}

# STEP 2: Create a block
block = {
    "number": 1,
    "transactions": [
        {"sender": "Alice", "receiver": "Bob", "amount": 3},
        {"sender": "Bob", "receiver": "Emma", "amount": 2}
    ],
    "previous_hash": "0000"
}

# STEP 3: Display block information
print("=== BLOCK INFORMATION ===")
print("Block number:", block["number"])
print("Previous hash:", block["previous_hash"])

print("\n=== STARTING BALANCES ===")
print(balances)

# STEP 4: Display transactions
print("\n=== TRANSACTIONS INSIDE THE BLOCK ===")

for transaction in block["transactions"]:
    print("Sender:", transaction["sender"])
    print("Receiver:", transaction["receiver"])
    print("Amount:", transaction["amount"])
    print("------------------------")

# STEP 5: Create temporary balances
temporary_balances = balances.copy()
block_is_valid = True

# STEP 6: Validate every transaction
print("\n=== VALIDATING BLOCK TRANSACTIONS ===")

for transaction in block["transactions"]:
    print("\nChecking:", transaction)

    if validate_transaction(transaction, temporary_balances):
        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]

        temporary_balances[sender] -= amount
        temporary_balances[receiver] += amount

        print("Transaction accepted!")
        print("Temporary balances:", temporary_balances)

    else:
        block_is_valid = False
        print("Invalid transaction! Rejecting the block.")
        break

# STEP 7: Accept or reject the block
if block_is_valid:
    balances = temporary_balances
    print("\n=== BLOCK ACCEPTED ===")
else:
    print("\n=== BLOCK REJECTED ===")

# STEP 8: Display final balances
print("\n=== FINAL BALANCES ===")
print(balances)

# STEP 9: Calculate block hash
block_text = json.dumps(block, sort_keys=True)
block_bytes = block_text.encode("utf-8")
block_hash = hashlib.sha256(block_bytes).hexdigest()

print("\n=== BLOCK HASH ===")
print(block_hash)
