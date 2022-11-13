import json
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
curUser = BlockchainClient()

survey = Survey(sampleCreator, 'Personal Info Survey')
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
    curUser,
    incentive
)
t.sign_transaction()
transactions.append(t)

chain.add_block(transactions)
chain.update_chain()