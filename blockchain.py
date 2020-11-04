from functools import reduce
import hashlib as hl
import json
import pickle

from utility.hash_util import hash_block
from block import Block
from transactions import Transaction
from utility.verification import Verification
#this is how json look like
# {
#     "field": "value",
#     "field": [
#         {}
#     ]
# }
# initializing blockchain list
MINING_REWARD = 10

print(__name__)

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)

        self.chain = [genesis_block]
        self.__open_transaction = []
        self.load_data()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_transactions(self):
        return self.__open_transaction[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                #print(file_content)
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transaction']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain    
                open_transaction = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transaction:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.open_transaction = updated_transactions

        except (IOError,IndexError):
            pass
        finally:
            print("cleanup!")    


    def save_data(self):
        try: 
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transaction], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n') 
                saveable_tx = [tx.__dict__ for tx in self.__open_transaction]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot':open_transaction
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving Failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1] 
        last_hash = hash_block(last_block)
        proof= 0
        while not Verification.valid_proof(self.__open_transaction, last_hash, proof):
            proof += 1
        return proof    



    def get_balance(self):
        participants = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transaction if tx.sender == participants] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transaction if tx.sender == participants]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transaction if tx.recipient == participants] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum +  0, tx_recipient, 0)
        #Reaturn the total balance availabe
        return amount_received-amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain"""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self, recipient, sender, amount=1.0):
        """ Append a new value and the last blockchain value to the blockchain
        
        Arguments:
            :transaction_amount: The ampount that shuld be added.
            :last_transaction: The last blockchain transaction (default[1]).
        """
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        transaction = Transaction(sender, recipient, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transaction.append(transaction)
            self.save_data()
            return True
        return False    
            
        


    def mine_block(self):
        try:
            last_block = self.__chain[-1]
            hashed_block = hash_block(last_block) 
            proof = self.proof_of_work() 
            reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
            copied_transaction = self.__open_transaction[:]
            copied_transaction.append(reward_transaction)
            block = Block(len(self.__chain), hashed_block, copied_transaction, proof)
            self.__chain.append(block)
            self.__open_transaction = []
            self.save_data()
            return True  

        except IOError:
            print('Okay!')





   




