import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_hist(user_survey_result):
#if __name__ == '__main__':

    #user_survey_result = [0,0,0,0,0]
    ############### dummy data ###############

    q1 = ('Please select the\n age of your cat.')
    q1_choices = ([
            '3~6 months', 
            '6 moths ~1 year', 
            '1~3 years', 
            '3~6 years',
            '6~10 years',
            '+10 years',
            'not sure'
    ])
    q1_answers = ([1,1,4,1,1,2,0])

    q2 = ("What is your cat's\n favorite type of toy?")
    q2_choices = ([
            'Fishing rod / kasha kasha',
            'Doll',
            'Ball',
            'Food puzzle',
            'Tunnel',
            'else'
    ])
    q2_answers = ([3,1,1,2,1,2])

    q3 = ('How many times a day do you \nplay with your cat with toys?')
    q3_choices = ([
            'once or less',
            'twice',
            'thrice',
            'four times of more'
    ])
    q3_answers = ([3,4,2,1])

    q4 = ('How long do you play \nwith your cat per time?')
    q4_choices = ([
            'ten minutes or less',
            '10~20 minutes',
            '20~30 minutes',
            'more than 30 minutes'
    ])
    q4_answers = ([8,2,0,0])

    q5 = ("What is your cat's \nfavorite type of treat?")
    q5_choices = ([
            'Can',
            'Chur',
            'Treat',
            'Dried food',
            'else'
    ])
    q5_answers = ([1,7,1,1,0])

    q6 = ('How many time do you\n feed your cat?')
    q6_choices = ([
            'twice or less',
            'thrice',
            'four times',
            'five times',
            'six times or more'
    ])
    q6_answers = ([6,4,0,0,0])

    serveys = [q1, q2, q3, q4, q5, q6]
    choices = [q1_choices, q2_choices, q3_choices, q4_choices, q5_choices, q6_choices]
    answers = [q1_answers, q2_answers, q3_answers, q4_answers, q5_answers, q6_answers]

    #############################################

    res = []
    fig, axx = plt.subplots(nrows=1, ncols=6)

    for i in range(len(user_survey_result)):

        curr_ans = user_survey_result[i]
        #print(curr_ans)
        answers[i][curr_ans] = answers[i][curr_ans]+1 # increase hit num
        #print(choices[i], answers[i])

        #res.append(dict(zip(choices[i], answers[i])))
        res = dict(zip(choices[i], answers[i]))

        #print(res)
        
        df = pd.DataFrame(data = [res])

        #print(df)
        ax = axx[i]

        sns.barplot(data = df,ax=ax)
        ax.tick_params(axis='x', rotation=90)
        ax.set_title(serveys[i])

    plt.title('Survey result')
    plt.tight_layout()
    #plt.savefig('./survey_result.png')
    plt.show()