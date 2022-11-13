class SurveyQuestion: # node
    def __init__(self, question=""):
        self.question = question
        if type(question) is not str:
            self.question = ""
        self.answer = {}
        self.userChoice = 0

        self.nextVal = None
        self.index = 0
        
    def set_next(self, node):
        # if type(node) is not SurveyQuestion:
        #     print('SurveyQuestion.set_next :', 'input node only')
        #     return
        self.nextVal = node

class Survey:
    def __init__(self, name) -> None:
        # class attributes
        self.name = name
        self.thumbnail = ""
        self.description = ""

        # linked list implementation
        self.head = None
        self.length = 1
    
    ####################################################################
    ################### Class Attribute Functions ######################
    ####################################################################

    def set_thumbnail(self, url):
        self.thumbnail = url
        
    def set_description(self, description):
        self.description = description

    ####################################################################
    ###################### Linked List Functions #######################
    ####################################################################
        
    # for debugging purposes only
    def print_llist(self):
        print('<', self.name, '>')

        curQ = self.head
        print(curQ.index+1, ' :', curQ.question)

        while curQ.nextVal is not None:
            curQ = curQ.nextVal
            print(curQ.index+1, ' :', curQ.question)
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
    q2 = SurveyQuestion('How old are you?')
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