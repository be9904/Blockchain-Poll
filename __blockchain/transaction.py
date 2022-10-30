import hashlib
import random
import string
import json
import binascii
import logging
import datetime
import collections

class Transaction():
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

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