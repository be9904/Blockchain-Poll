class Survey:
    def __init__(self, name):
        self.name = name
        self.thumbnail = ""
        self.description = ""
        self.questions = []
        
    def set_thumbnail(self, link):
        self.thumbnail = link
        
    
        
class SurveyQuestion:
    def __init__(self):
        self.question = ""
        self.answer = []
        self.userChoice = 0

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
    def __init__(self, node):
        if type(node) is not Node:
            print('input node only')
            return
        self.head = node
        self.length = 1
        
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
        
        # set default index to last item of llist
        if index == None:
            index = self.length-1
            
        # return if input node is not of type Node
        if type(node) is not Node:
            print('input node only')
            return    
        
        # return if given index is out of bounds
        if index > self.length-1:
            print('index out of bounds')
            return
        
        # traverse through llist
        while curNode.index < index:
            curNode = curNode.nextVal
        
        # exception handling
        if curNode == None:
            print('check llist pointers')
            return
        
        # append item and update llist
        node.nextVal = curNode.nextVal
        if curNode.nextVal is not None:
            curNode.nextVal.index += 1
        
        curNode.nextVal = node
        node.index = index+1
        self.length += 1
        
        
a = Node(3)
b = Node(5)
c = Node(8)
d = Node(19)
e = Node(88)

llist = IndexedLinkedList(a)
llist.print_llist()

llist.append(b)
llist.print_llist()

llist.append(c)
llist.print_llist()

llist.append(d, 1)
llist.print_llist()

llist.append(e, 1)
llist.print_llist()