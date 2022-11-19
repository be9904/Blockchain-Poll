class Survey:
    def __init__(self, name):
        self.name = name
        self.thumbnail = ""
        self.description = ""
        self.questions = IndexedLinkedList()
        
    def set_thumbnail(self, link):
        self.thumbnail = link
        
    def set_description(self, description):
        self.description = description
        
    def add_question(self, question):
        # if type(question) is not SurveyQuestion:
        #     print('type \'SurveyQuestion\' is required')
        #     return
        
        self.questions.append(question)
        
class SurveyQuestion:
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

###################################################################
######################### Data Structure ##########################
###################################################################

class Node:
    def __init__(self, data=None):
        self.data = data
        self.nextVal = None
        self.index = 0
        
    def set_next(self, node):
        if type(node) is not Node:
            print('input node only')
            return
        self.nextVal = node
    
class IndexedLinkedList:
    def __init__(self):
        self.length = 1
        self.head = None
        
    # for debugging purposes only
    def print_llist(self):
        curNode = self.head
        print(curNode.data, end=' ')
        
        while curNode.nextVal is not None:
            curNode = curNode.nextVal
            print(curNode.data, end=' ')
        print()
        
    def append(self, node, index=None):
        curNode = self.head
        
        if curNode is None:
            self.head = node
            return
        
        # set default index to last item of llist
        if index == None:
            index = self.length-1
            
        # return if input node is not of type Node
        if type(node) is not Node:
            print('append:','input node only')
            return    
        
        # return if given index is out of bounds
        if index > self.length-1:
            print('append:','index out of bounds')
            return
        
        # traverse through llist
        while curNode.index < index:
            curNode = curNode.nextVal
        
        # exception handling
        if curNode == None:
            print('append:','check llist pointers')
            return
        
        # append item and update llist
        node.nextVal = curNode.nextVal
        if curNode.nextVal is not None:
            curNode.nextVal.index += 1
        
        curNode.nextVal = node
        node.index = index+1
        self.length += 1
        
        
# a = Node(3)
# b = Node(5)
# c = Node(8)
# d = Node(19)
# e = Node(88)

# llist = IndexedLinkedList(a)
# llist.print_llist()

# llist.append(b)
# llist.print_llist()

# llist.append(c)
# llist.print_llist()

# llist.append(d, 1)
# llist.print_llist()

# llist.append(e, 1)
# llist.print_llist()

survey = Survey('Test')
q1 = Node(SurveyQuestion('Hello?'))
q2 = Node(SurveyQuestion('Hi?'))

survey.add_question(q1)
survey.add_question(q2)

survey.questions.print_llist()

# for q in survey.questions:
#     print(q.question)