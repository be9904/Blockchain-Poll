import json
from user import *
from survey import *
from blockchain import *
from tcp import client, server

chain = Blockchain()
incentive = 2.0
sampleCreator = BlockchainClient()

# server should be running
# c = client.LocalClient()
# c.client_main()

# Login Sequence -> replace tcp
curUser = User(BlockchainClient(), 'yuljeoni')

survey = Survey(sampleCreator, 'Personal Info Survey', 5.0)
q1 = SurveyQuestion('What is your name?')
q1.set_choices(['John', 'Joe', 'Sharon', 'Helen'])
q2 = SurveyQuestion('How old are you?')
q2.set_choices([20, 21, 22, 23, 24, 25])
q3 = SurveyQuestion('What is your major?')
q4 = SurveyQuestion('What is your hobby?')
q5 = SurveyQuestion('Where do you live?')

survey.add_question(q1)
survey.add_question(q2)
survey.add_question(q3)
survey.add_question(q4, 1)
survey.add_question(q5, 4)
survey.print_llist()

# On Start Survey Click
if survey.check_participation(curUser) is False:
    print('Start Survey')
else:
    print('already participated')

# On Submit Click
transactions = []
t = Transaction(
    sampleCreator,
    curUser.client,
    incentive
)
t.sign_transaction()
transactions.append(t)

# chain.add_block(transactions)
# chain.update_chain()

# On View Survey Click
if curUser.balance < survey.view_cost:
    print('not enough coins')
else:
    t = Transaction(
        curUser.client,
        sampleCreator,
        survey.view_cost
    )
    t.sign_transaction()
    transactions.append(t)
    
chain.add_block(transactions)
chain.update_chain()