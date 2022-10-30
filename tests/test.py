import json
import datetime
import hashlib

registered_users = {
    "skku" : {
        "pw" : "1111",
        "Name" : "율전이",
        "index" : 0,
        "timestamp" : "2022-10-30 13:25:00.024478"
    }
}

block = registered_users['skku']
block = json.dumps(block, sort_keys=True).encode()
hash = hashlib.sha256(block).hexdigest()
print(block)
print(hash)

print(datetime.datetime.now())

def add(a, b):
    return a+b

x = add(
    1,
    2
)

print(x)