import json
from survey import *
from blockchain import *
from tcp import client, server

# server should be running
c = client.LocalClient()

survey = Survey('Personal Info Survey')
q1 = SurveyQuestion('What is your name?')
q2 = SurveyQuestion('How old are you?')
q3 = SurveyQuestion('What is your major?')
q4 = SurveyQuestion('What is your hobby?')
q5 = SurveyQuestion('Where do you live?')

survey.add_question(q1)
survey.add_question(q2)
survey.add_question(q3)
survey.add_question(q4, 1)
survey.add_question(q5, 4)
survey.print_llist()