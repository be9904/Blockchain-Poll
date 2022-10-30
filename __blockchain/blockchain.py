import datetime
import hashlib
import json

class BlockChain():

    def __init__(self, init):
        self.chain = []
        if init != None:
            self.add_block(init)
    
    # add block and append to chain
    def add_block(self, proof, previous_hash):
        block = {
            "index" : len(self.chain) + 1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash
        }
        self.chain.append(block)
        return block
    
    # proof of work
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        
        return new_proof
    
    # generate hash
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # check chain validity
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_op = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_op[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        
        return True