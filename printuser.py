import json
from user import *
from survey import *
from blockchain import *
import ast

admin = User(BlockchainClient(), 'admin')
yuljeoni = User(BlockchainClient(), 'yuljeoni')
myeongnyuni = User(BlockchainClient(), 'myeongnyuni')

a_dict = ast.literal_eval(json.dumps(admin, indent=4, cls=UserEncoder))
y_dict = ast.literal_eval(json.dumps(yuljeoni, indent=4, cls=UserEncoder))
m_dict = ast.literal_eval(json.dumps(myeongnyuni, indent=4, cls=UserEncoder))

d = {}
d['admin'] = a_dict
d['yuljeoni'] = y_dict
d['myeongnyuni'] = m_dict

json_file = open('./tcp/users.json', 'w')
json.dump(d, json_file)