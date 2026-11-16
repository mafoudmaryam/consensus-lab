
# CONSENSUS LAB - DAY 6
# Experiment: Reject a block with a broken hash connection

import hashlib
import json
from transaction_validator import validate_transaction

balances = {
    "Alice": 10,
    "Bob": 5,
    "Emma": 2
}

blockchain = []


def calculate_hash(block):
    block_text = json.dumps(block, sort_keys=True)
    return hashlib.sha256(block_text.encode("utf-8")).hexdigest()


def add_block(block):
    print("\n=== CHECKING BLOCK", block["number"], "===")

    if len(blockchain) == 0:
        expected_previous_hash = "0000"
    else:
        expected_previous_hash = calculate_hash(blockchain[-1])

    if block["previous_hash"] != expected_previous_hash:
        print("BLOCK REJECTED: Wrong previous hash!")
        return False

    temporary_balances = balances.copy()

    for transaction in block["transactions"]:
        if not validate_transaction(transaction, temporary_balances):
            print("BLOCK REJECTED: Invalid transaction!")
            return False

        sender = transaction["sender"]
        receiver = transaction["receiver"]
        amount = transaction["amount"]

        temporary_balances[sender] -= amount
        temporary_balances[receiver] += amount

    balances.update(temporary_balances)
    blockchain.append(block)

    print("BLOCK ACCEPTED!")
    return True


# Block 1: Correct starting block
block1 = {
    "number": 1,
    "transactions": [
        {"sender": "Alice", "receiver": "Bob", "amount": 3},
        {"sender": "Bob", "receiver": "Emma", "amount": 2}
    ],
    "previous_hash": "0000"
}

add_block(block1)


# Block 2: Intentionally wrong previous hash
block2 = {
    "number": 2,
    "transactions": [
        {"sender": "Emma", "receiver": "Alice", "amount": 1}
    ],
    "previous_hash": "WRONG_HASH"
}

add_block(block2)


print("\n=== FINAL BLOCKCHAIN LENGTH ===")
print(len(blockchain))

print("\n=== FINAL BALANCES ===")
print(balances)
