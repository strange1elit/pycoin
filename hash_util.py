import hashlib as hl
import json 
from transactions import Transaction



def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transaction'] = [tx.to_ordered_dict() for tx in hashable_block['transaction']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode()) # sha256 (json.dumps(block) will create a string
     # use encode() to really encode it to utf-8                                     
     # the above hash we have generated is not a string (it's a byte hash) so we call hexdigest() method to convert it into string or normal chatrecters