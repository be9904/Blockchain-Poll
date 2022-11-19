# node
class SurveyQuestion:
    def __init__(self, question=""):
        self.question = question
        # if type(question) is not str:
        #     self.question = ""
        self.answer = []
        self.userChoice = -1

        self.nextVal = None
        self.index = 0

    def set_choices(self, choices):
        for choice in choices:
            self.answer.append((choice, False))

    def choose_option(self, index):
        # reset choice
        for i in range(len(self.answer)):
            c = self.answer[i][0]
            self.answer[i] = (c, False)
        
        # choose option
        self.answer[index] = (self.answer[index][0], True)
        
    def set_next(self, node):
        # if type(node) is not SurveyQuestion:
        #     print('SurveyQuestion.set_next :', 'input node only')
        #     return
        self.nextVal = node

    def print_question(self):
        print(str(self.index+1)+'.', self.question)
        for answer in self.answer:
            print('\t*', answer[0])

# linked list
class Survey:
    def __init__(self, creator, name, view_cost=0) -> None:
        # class attributes
        self.creator = creator
        self.name = name
        self.thumbnail = ""
        self.description = ""
        self.participants = {}
        self.view_cost = view_cost

        # linked list implementation
        self.head = None
        self.length = 1
    
    ####################################################################
    ################### Class Attribute Functions ######################
    ####################################################################

    def set_thumbnail(self, path):
        self.thumbnail = path
        
    def set_description(self, description):
        self.description = description

    def add_participant(self, user):
        self.participants[user] = True
    
    def check_participation(self, user):
        if self.participants.get(user) is None:
            return False
        else:
            return True

    ####################################################################
    ###################### Linked List Functions #######################
    ####################################################################
        
    # for debugging purposes only
    def print_llist(self):
        print('<', self.name, '>')

        curQ = self.head
        curQ.print_question()

        while curQ.nextVal is not None:
            curQ = curQ.nextVal
            curQ.print_question()
        print()

    # add question(node) to llist
    def add_question(self, question, index=None):
        # if type(question) is not SurveyQuestion:
        #     print('type \'SurveyQuestion\' is required')
        #     return
        curQ = self.head

        if curQ is None:
            self.head = question
            return

        # set default append index to last item of llist
        if index == None:
            index = self.length-1
        else:
            index -= 2
        

        # set question to head
        if index == -1:
            question.set_next(self.head)
            question.index = 0
            self.head = question

            while curQ.index < self.length-1:
                curQ.index += 1
                curQ = curQ.nextVal

            curQ.index += 1
            self.length += 1
            
            return

        # return if input node is not of type SurveyQuestion
        if type(question) is not SurveyQuestion:
            print('Survey.add_question :','input \'SurveyQuestion\' only')
            return
        
        # return if given index is out of bounds
        if index > self.length-1:
            print('Survey.add_question :', 'given index out of bounds')
            return

        # traverse llist
        while curQ.index < index:
            curQ = curQ.nextVal

        # exception handling
        if curQ == None:
            print('Survey.add_question :', 'error in llist pointers')

        # append item and update list
        question.set_next(curQ.nextVal)
        if curQ.nextVal is not None:
            curQ.nextVal.index += 1

        curQ.set_next(question)
        question.index = index+1
        self.length += 1

if __name__ == "__main__":
    survey = Survey('Personal Info Survey')

    q1 = SurveyQuestion('What is your name?')
    q1.set_choices(['John', 'Joe', 'Sharon', 'Helen'])
    q2 = SurveyQuestion('How old are you?')
    q2.set_choices([20, 21, 22, 23, 24, 25])
    q3 = SurveyQuestion('What is your major?')
    q4 = SurveyQuestion('What is your hobby?')
    q5 = SurveyQuestion('Where do you live?')

    survey.add_question(q1)
    survey.print_llist()

    survey.add_question(q2)
    survey.print_llist()

    survey.add_question(q3)
    survey.print_llist()

    survey.add_question(q4, 1)
    survey.print_llist()

    survey.add_question(q5, 4)
    survey.print_llist()