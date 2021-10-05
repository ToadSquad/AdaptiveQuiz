# AdaptiveQuiz.py
# Original CLI File, see RebuildAdaptiveQuiz.py for Proper WebApp Integration
# Creators: Angel LaVoie, Suman Panta, Sankalpa Kattel

import csv
import random
import re

from itertools import islice

## Questions.csv is Original CSV, Questions_1.csv is Difficulty Tracking CSV

class Question:
    def __init__(self, ques, ans):
        self.ques=ques
        self.ans=ans

# Pull Questions from CSV
prompts=[]

# Assign Correct Answer from CSV
answers=[]

# Pull Options for Wrong Answers from CSV
options=[]

# Pull Score of User
player_score=0

## Pull Score from File Here

# Tracking Current Session Score
current_score=player_score

with open('Questions_1.csv', newline='') as csvfile:
    lreader=csv.reader(csvfile, delimiter=',', quotechar='|')
    ansidx=None
    randidx=None
    for row in lreader:
        try:
            if row[0].__contains__('{'):
                    #fishing for variant questions
                    questionChoice=re.search(r"\{([A-Za-z0-9_\/]+)\}",row[0])
                    questionChoiceString=questionChoice.group(1)
                    questionChoiceSplit=questionChoiceString.split('/')
                    randVariant=random.choice(questionChoiceSplit)
                    randidx=questionChoiceSplit.index(randVariant)
                    row[0]=row[0].replace(questionChoiceString, randVariant)
                    row[0]=row[0].replace('{','')
                    row[0]=row[0].replace('}','')
            prompts.append(row[0])

            for cell in row:
                if cell.__contains__('Answer'):
                    ansidx=row.index(cell)
                if cell.__contains__('Option'):
                    options.append(row.index(cell))

            if row[ansidx].__contains__('{'):
                    #fishing for the variant answer based on what variant question was chosen
                    answerChoice=re.search(r"\{([A-Za-z0-9_\.\;\(\)\/]+)\}",row[ansidx])
                    answerChoiceString=answerChoice.group(1)
                    answerChoiceSplit=answerChoiceString.split('/')
                    answerChoiceFinal=answerChoiceSplit[randidx]
                    row[ansidx]=row[ansidx].replace(answerChoiceString, answerChoiceFinal)
                    row[ansidx]=row[ansidx].replace('{','')
                    row[ansidx]=row[ansidx].replace('}','')
            answers.append(row[ansidx])
        except IndexError:
            print('List Complete')

# Start at Right Place Based on Score
medium_threshold=9
high_threshold=14
score_threshold='easy'

# Removing Prompts and Answers for Start Based on Score
if player_score>=medium_threshold and player_score<high_threshold:
    score_threshold='medium'
    prompts=prompts[16:]
    answers=answers[16:]
if player_score>=high_threshold:
    score_threshold='high'
    prompts=prompts[23:]
    answers=answers[23:]

# Connecting Correct Answer to Prompt
questions=[]
x=0
while x < len(prompts):
    #questions.append("Question(prompts[{}], answers[{}])".format(x, x))
    questions.append(Question(prompts[x], answers[x]))
    x+=1


# Every time you rotate to a new question, grab the random answers to use and display
def run(questions, current_score):
    with open('Questions_1.csv', newline='') as csvfile:
        x=0
        if score_threshold=='medium':
            x=16
        if score_threshold=='high':
            x=23
        #df=pd.read_csv('Questions_1.csv', skiprows=x, delimiter=',', quotechar='|')
        lreader=csv.reader(islice(csvfile, x, None), delimiter=',', quotechar='|')
        for question, row in zip(questions, lreader):
            try:
                if "Question" in row[0]:
                    continue
                if "Assigned Difficulty" in row[0]:
                    continue
                if len(row[0])==0:
                    continue
                aux=options.copy()
                choices=[]
                for i in range(3): #randomizing what 3 of the 6 wrong answers to use
                    randchoice=random.choice(aux)
                    idx=aux.index(randchoice)
                    choices.append(row[randchoice])
                    del aux[idx]
                choices.append(question.ans)
                promptorder=[]
                for j in range(4): #randomizing choices altogether with correct answer
                    choice=random.choice(choices)
                    idx=choices.index(choice)
                    promptorder.append(choice)
                    del choices[idx]
                prompt=question.ques+"\n(1) {}\n(2) {}\n(3) {}\n(4) {}\n".format(promptorder[0], promptorder[1], promptorder[2], promptorder[3])
                selection=prompt.split('\n') #deleting the question itself from selection array
                del selection[0]
                del selection[4]
                answer=input(prompt) #getting input from user for answer
                actans=selection[(int(answer)-1)] #checking against selection array
                if question.ans in actans:
                    print('Correct!')
                    current_score+=1
                else:
                    print('Incorrect!')
            except IndexError:
                print('List Complete')
        ## Save Score to File Here


run(questions, current_score)

