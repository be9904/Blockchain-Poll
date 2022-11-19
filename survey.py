# node
class SurveyQuestion:
    def __init__(self, question=""):
        self.question = question
        # if type(question) is not str:
        #     self.question = ""
        self.answer = []
        self.userChoice = 0

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
        self.userChoice = index
        
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

def CreateSample():
    survey = Survey('sampleCreator', '고양이 설문')

    q1 = SurveyQuestion('고양이의 연령대를 선택해주세요.')
    q1.set_choices([
        '3~6개월', 
        '6개월~1살', 
        '1살~3살', 
        '3살~6살',
        '6살~10살',
        '10살 이상',
        '모름'])
    q2 = SurveyQuestion('고양이가 가장 선호하는 형태의 장난감은 무엇인가요?')
    q2.set_choices([
        '낚싯대/카샤카샤',
        '인형',
        '공',
        '먹이퍼즐',
        '터널',
        '기타'])
    q3 = SurveyQuestion('하루에 고양이를 장난감으로 놀아주는 횟수는 몇 번인가요?')
    q3.set_choices([
        '1번 이하',
        '2번',
        '3번',
        '4번 이상'
    ])
    q4 = SurveyQuestion('한 번 고양이와 놀아줄 때 놀이를 몇 분 지속하나요?')
    q4.set_choices([
        '10분 미만',
        '10~20분',
        '20~30분',
        '30분 초과'])
    q5 = SurveyQuestion('고양이가 가장 선호하는 형태의 간식은 무엇인가요?')
    q5.set_choices([
        '캔',
        '츄르',
        '트릿',
	    '말린 형태',
        '기타'
    ])
    q6 = SurveyQuestion('고양이에게 간식을 포함한 급여는 하루에 몇 번 인가요?')
    q6.set_choices([
        '2번 이하',
        '3번',
        '4번',
	    '5번',
	    '6번 이상'
    ])

    survey.add_question(q1)
    survey.add_question(q2)
    survey.add_question(q3)
    survey.add_question(q4)
    survey.add_question(q5)
    survey.add_question(q6)
    # survey.print_llist()
    return survey