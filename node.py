import time, threading
from blockchain import Blockchain, Transaction
from utils import new_block_log, read_from_file

BOLCK_TIME = 10

class Node():
    def __init__(self):
        self.blockchain = Blockchain()
        self.current_block = self.blockchain.create_block()
        self.start_time = time.time()
        self.stop_flag = False

    def scan_tx(self):
        while True:
            if self.stop_flag:
                break

            elapse = time.time() - self.start_time
            if elapse > BOLCK_TIME: # generate a new block
                self.start_time = time.time()
                self.blockchain.add_block(self.current_block)

                new_block_log(self.current_block, self.blockchain.state)

                self.current_block = self.blockchain.create_block()

            if self.blockchain.tx_pool:
                tx = self.blockchain.tx_pool.popleft()

                from_account = self.blockchain.state.get_account(tx.from_address)
                tx.nonce = from_account.get_nonce()
                tx.hash = tx.hash_tx()

                # verify tx
                if from_account.get_balance() < tx.amount:
                    print("invalid tx: balance not enough")
                else:
                    self.current_block.add_transaction(tx)
                    self.blockchain.state.change_state(tx)
            else:
                time.sleep(0.3)

    def run(self):
        self.thread = threading.Thread(target=self.scan_tx)
        self.thread.start()

    def stop(self):
        self.stop_flag = True
        self.thread.join()


if __name__ == '__main__':
    node = Node()
    node.run()

    print("input (file name or stop):")
    while True:
        input_str = input()

        if input_str == "stop":
            node.stop()
            break

        txs = read_from_file(input_str)
        for tx in txs:
            from_adress, to_address, amount = tx
            from_account = node.blockchain.state.get_account(from_adress)

            raw_tx = Transaction(from_adress, to_address, amount)
            node.blockchain.tx_pool.append(raw_tx)
