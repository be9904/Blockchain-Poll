from json import JSONEncoder

class User:
    def __init__(self, client, name) -> None:
        self.client = client
        self.name = name
        self.balance = 100.0

    def get_balance(self):
        return self.balance

    def update_balance(self, delta):
        self.balance = self.balance + delta

class UserEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__