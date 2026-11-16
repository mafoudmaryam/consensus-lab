
# CONSENSUS LAB - DAY 4
# Transaction Validation and Double-Spending Experiment

# STEP 1: Starting balances
balances = {
    "Alice": 10,
    "Bob": 5,
    "Emma": 2
}

# STEP 2: Create two example transactions
transactions = [
    {"sender": "Alice", "receiver": "Bob", "amount": 6},
    {"sender": "Alice", "receiver": "Emma", "amount": 5}
]


# STEP 3: Define our transaction validation function
def validate_transaction(transaction, balances):
    sender = transaction["sender"]
    receiver = transaction["receiver"]
    amount = transaction["amount"]

    if sender not in balances:
        print("Rejected: Sender does not exist.")
        return False

    if receiver not in balances:
        print("Rejected: Receiver does not exist.")
        return False

    if type(amount) is not int or amount <= 0:
        print("Rejected: Amount must be a positive integer.")
        return False

    if balances[sender] < amount:
        print("Rejected: Not enough coins.")
        return False

    print("Transaction passed the balance rules!")
    return True


# STEP 4: Run the Day 4 experiment only when this file
# is executed directly, not when imported by another file
if __name__ == "__main__":

    print("=== BEFORE TRANSACTIONS ===")
    print(balances)

    for transaction in transactions:
        print("\n=== CHECKING TRANSACTION ===")
        print(transaction)

        if validate_transaction(transaction, balances):
            sender = transaction["sender"]
            receiver = transaction["receiver"]
            amount = transaction["amount"]

            balances[sender] -= amount
            balances[receiver] += amount

            print("Transaction completed successfully!")
        else:
            print("Transaction was not executed.")

    print("\n=== AFTER TRANSACTIONS ===")
    print(balances)
