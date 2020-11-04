from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
class Node:
    def __init__(self):
        #self.id = str(uuid4())
        self.id = 'MAX'
        self.blockchain = Blockchain(self.id)


    def get_transaction_value(self):
        """Returns the input of the user ( a new transaction amount ) as a float"""
        tx_recipient = input('Enter the recipient of the transaction : ')
        tx_amount = float(input('Please enter your transaction amount : '))
        return (tx_recipient, tx_amount)



    def get_user_choice(self): 
        user_input = input('Your choice : ')
        return user_input

    def print_blockchain_elements(self):
        #Output the blockchain list to the console 
        for block in self.blockchain.chain:
            print('Outputting Block')
            print(block)
        else:
            print('--'*20)




    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please choose :')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: check transaction validity')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print('Added Transaction') 
                else:
                    print('Transaction Failed')
                    print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                verifier = Verification()  
                if verifier.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transaction are valid') 
                else:
                    print('There are invalid transaction')     
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid,please pick a value from the list! ')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break 
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))

        else:
            print('User Left!')


        print('Done!')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
