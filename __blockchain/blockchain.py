import binascii
import collections
import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from datetime import datetime
from hashlib import sha256

# single block in a blockchain
class Block:
    def __init__(self, transactions, previous_hash, nonce = 0):
        self.timestamp = datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.generate_hash()

    def print_block(self):
        # prints block contents
        print("timestamp:", self.timestamp)
        print("transactions:", self.transactions)
        print("current hash:", self.generate_hash())

    def generate_hash(self):
        # hash the blocks contents
        block_contents = str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)
        block_hash = sha256(block_contents.encode())
        return block_hash.hexdigest()

# definition of blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        # self.all_transactions = []
        self.genesis_block()
    
    def genesis_block(self):
        if len(self.chain) == 0:
            transactions = []
            block = Block(transactions, 0)
            self.chain.append(block)
            return self.chain

    # prints contents of blockchain
    def print_blocks(self):
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            print("Block {} {}".format(i, current_block))
            current_block.print_block()

    def add_block(self, transactions):
        previous_block_hash = self.chain[len(self.chain)-1].hash
        new_block = Block(transactions, previous_block_hash)
        proof = self.proof_of_work(new_block)
        self.chain.append(new_block)
        return proof, new_block

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.generate_hash():
                print("The current hash of the block does not equal the generated hash of the block.")
                return False
            if previous.hash != previous.generate_hash():
                print("The previous block's hash does not equal the previous hash value stored in the current block.")
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
  
    def proof_of_work(self, block, difficulty=2):
        proof = block.generate_hash()

        while proof[:2] != '0'*difficulty:
            block.nonce += 1
            proof = block.generate_hash()
        return proof

# blockchain client info
class BlockchainClient():
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.export_key(format='DER')).decode('ascii')

# define a transaction
class Transaction():
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.now()

    def convert_to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

        return collections.OrderedDict({
            'sender' : identity,
            'recipient' : self.recipient,
            'value' : self.value,
            'time' : self.time
        })
    
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.convert_to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

# print transaction in readable format
def display_transaction(transaction):
   dict = transaction.convert_to_dict()
   print ("sender: " + dict['sender'])
   print ('-----')
   print ("recipient: " + dict['recipient'])
   print ('-----')
   print ("value: " + str(dict['value']))
   print ('-----')
   print ("time: " + str(dict['time']))
   print ('-----')

# test run
if __name__ == '__main__':
    user = BlockchainClient()
    print (user.identity)

    print('*****************************************************************************************')
    
    poll = Blockchain()

    transactions = []
    
    transaction1 = {
        'sender': 'Messi',
        'receiver': 'Ronaldo',
        'amount': 1000,
    }
    transactions.append(transaction1)

    transaction2 = {
        'sender': 'Ronaldo',
        'receiver': 'Messi',
        'amount': 50,
    }
    transactions.append(transaction2)

    transaction3 = {
        'sender': 'Messi',
        'receiver': 'Son',
        'amount': 8000,
    }
    transactions.append(transaction3)

    poll.add_block(transactions)
    poll.print_blocks()