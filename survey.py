class SurveyQuestion: # node
    def __init__(self, question):
        self.question = question
        if type(question) is not str:
            self.question = ""
        self.answer = {}
        self.userChoice = 0
        
    def append(self, choice):
        if type(choice) is not str:
            print('type \'str\' is required')
            return
        id = len(self.answer)-1 if len(self.answer) > 0 else 0
        self.answer[id] = choice

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
        curQ = self.head
        print(curQ.question)

        while curQ.nextVal is not None:
            curQ = curQ.nextVal
            print(curQ.index, ' :', curQ.question)
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

        # return if input node is not of type SurveyQuestion
        if type(question) is not SurveyQuestion:
            print('add_question:','input \'SurveyQuestion\' only')
            return
        
        # return if given index is out of bounds
        if index > self.length-1:
            print('add_question:', 'given index out of bounds')
            return

        # traverse llist
        while curQ.index < index:
            curQ = curQ.nextVal

        # exception handling
        if curQ == None:
            print('add_question:', 'error in llist pointers')

        # append item and update list
        question.nextVal = curQ.nextVal
        if curQ.nextVal is not None:
            curQ.nexVal.index += 1

        curQ.nexVal = question
        question.index = index+1
        self.length += 1

