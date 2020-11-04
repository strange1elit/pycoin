""""Provides verification helper methods."""

from utility.hash_util import hash_string_256, hash_block

class Verification:
    @staticmethod
    def valid_proof(transaction, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transaction]) + str(last_hash) + str(proof)).encode()
        
        guess_hash = hash_string_256(guess)
        
        return guess_hash[0:2] == '00'




    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid, False if not valid """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transaction[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True 

    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount

       

    @classmethod
    def verify_transactions(cls, open_transaction, get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transaction])
