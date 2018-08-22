import hashlib

from collections import deque
from state import State

class Blockchain():
    def __init__(self):
        self.tx_pool = deque()
        self.blocks = []
        self.state = State()

        # add genesis block
        b = Block("0", 0)
        b.hash = b.hash_block()
        self.add_block(b)

    def add_block(self, block):
        block.hash = block.hash_block()
        self.blocks.append(block)

    def create_block(self):
        prev_hash = self.blocks[-1].hash
        prev_height = self.blocks[-1].height

        return Block(prev_hash, prev_height+1)


class Block():
    def __init__(self, prev_hash, height):
        self.prev_hash = prev_hash
        self.height = height
        self.transactions = []
        self.transaction_hashes = []
        self.hash = None

    def hash_block(self):
        sha = hashlib.sha256()
        hash_str = str(self.prev_hash) + str(self.height)
        hash_str_encode = hash_str.encode('utf-8')
        sha.update(hash_str_encode)
        for tx_hash in self.transaction_hashes:
            sha.update(str(tx_hash).encode('utf-8'))

        return sha.hexdigest()

    def add_transaction(self, tx):
        self.transactions.append(tx)
        self.transaction_hashes.append(tx.hash)

    def dump(self):
        print("block height:", self.height)
        print("block hash:", self.hash)
        print("prev hash:", self.prev_hash)
        print("number of transactions:", len(self.transactions))
        print("tx_hashs:", self.transaction_hashes)
        for tx in self.transactions:
            print("tx: hash: {}, from_address: {}, to_address: {}, amount: {}" \
                   .format(tx.hash, tx.from_address, tx.to_address, tx.amount))


class Transaction():
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.nonce = None
        self.hash = None

    def hash_tx(self):
        sha = hashlib.sha256()
        hash_str = str(self.from_address) + str(self.to_address) + str(self.amount) + str(self.nonce)
        hash_str_encode = hash_str.encode('utf-8')
        sha.update(hash_str_encode)

        return sha.hexdigest()
