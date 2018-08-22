from collections import defaultdict

INITIAL_AMOUMT = 100.0

class State():
    def __init__(self):
        self.accounts = defaultdict()

    def set_initial_account(self, address):
        account = Account(address)
        self.accounts[address] = account

    def get_account(self, address):
        if address not in self.accounts:
            self.set_initial_account(address)

        return self.accounts[address]

    def change_state(self, tx):
        from_address = tx.from_address
        to_address = tx.to_address
        amount = tx.amount

        from_account = self.get_account(from_address)
        to_account = self.get_account(to_address)

        from_account.substract_balance(amount)
        from_account.increment_nonce()

        to_account.add_balance(amount)

    def dump(self):
        print("current state:")
        for address, account in self.accounts.items():
            print("address: {}, balance: {:.9f}, nonce: {}".format(address, account.balance, account.nonce))



class Account():
    def __init__(self, address):
        self.address = address
        self.balance = INITIAL_AMOUMT
        self.nonce = 0

    def get_balance(self):
        return self.balance

    def get_nonce(self):
        return self.nonce

    def add_balance(self, amount):
        self.balance += amount

    def substract_balance(self, amount):
        self.balance -= amount

    def increment_nonce(self):
        self.nonce += 1
