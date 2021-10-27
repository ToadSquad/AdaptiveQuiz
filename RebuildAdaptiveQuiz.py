# RebuildAdaptiveQuiz.py
# See AdaptiveQuiz.py for Original CLI code, re-written by Devin Salter for proper Web App Integration with Flask
# Creators: Devin Salter

# Make UI bigger, add Header

import csv, random, re, os
from itertools import islice
import threading, time, json, sys

from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask_session import Session
import mysql.connector

from datetime import timedelta






app = Flask(__name__)
app.secret_key = os.urandom(24)

#Sessioning
#SESSION_TYPE = 'sqlalchemy'

app.secret_key = 'waddup'
sessionsecret = 'hello'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=31)

#threads
threads = {}

closed = False # Flag for save_thread
save_thread = None # Contains the thread saving user information on interval
questions = [] # Holds Question objects
options = [2, 4, 6, 8, 10, 12] # Determines all the columns that contain options for answers
difficulty_markers = [0, 9, 14] # Marks where the first question in a given difficulty is
users = [] # Stores users here until db is up and running
current_questions = [] # Ties users to their current questions and deletes after
active_sessions = 0
user_data = {} # Stores user scores and performance
question_data = {} # Stores question data ex. times, accuracy 
activeUsers = {} # Stores users logged in
conn = None
cursor = None

class Question:
    def __init__(self, question, answer, options,catergory,diffculty):
        self.question = question # The prompt
        self.answer = answer # The correct answer
        self.options = options # Array with all options to choose from
        self.catergory = catergory
        self.diffculty = diffculty

class User:
    def __init__(self,username):
        self.username = username
        self.score = 0
        self.question = None
        self.questions = []
        self.kill_thread = False
        self.thread = None
        self.questionData = []
    
class CurrentQuestion:

    kill_thread = False

    def __init__(self, user, question):
        self.user = user
        self.question = question

    def __str__(self):
        return f'{self.user.cookie}, {self.question.question}'

def save_users_db():
    global cursor, conn
    #assuming user exists
    print("saving")
    for username in activeUsers:
        if(len(activeUsers[username].questionData)>0):
            for record in activeUsers[username].questionData:
                print('INSERT INTO userData VALUES (NULL,"'+record["prompt"]+'", "'+record["cat"]+'", '+str(record["length"])+', "'+username+'", '+str(record["correct"])+');')
                cursor.execute('INSERT INTO userData VALUES (NULL,"'+record["prompt"]+'", "'+record["cat"]+'", '+str(record["length"])+', "'+username+'", '+str(record["correct"])+');')
                conn.commit()
        activeUsers[username].questionData = []      

# Initiates a save every 2 minutes
def save_users_on_timer():
    # Timer portion from https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
    # by Dave Rove, used because it was more efficient than what we originally created
    start = time.time()
    while not closed:
        # Initiates a save every 2 minutes
        time.sleep(10 - (time.time() - start) % 10)
        start = time.time()
        #save_users()
        save_users_db()

def load_users_db():
    global cursor, conn
    cursor.execute('select * from users;')
    result = cursor.fetchall()
    for column in result:
        activeUsers[column[1]] =  User(column[1])
# Checks the given cell/string for a variant question, choosing randomly
                # Only occurs if there is an option built into the question
                # For right now, this is a copy paste until I can confirm
                #   it works.
#Get Database Login
def login_database():
    global cursor, conn
    try:
        conn = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='mysql')
        cursor = conn.cursor()
    except:
        print("connection unsucessful")
def get_questions():
    global cursor, conn
    cursor.execute('select * from question;')
    result = cursor.fetchall()
    for column in result:
        options_array = [column[1],column[2], column[3], column[4], column[5], column[6]]
        questions.append(Question(column[0],column[7],options_array,column[8],column[9]))

# Chooses a random question in the provided range
def get_question(min, max):
    return questions[random.choice(range(min, max))]

def choose_question(score):
    # Question chosen through ranomization within point thresholds
    chosen_question = None

    if score >= difficulty_markers[0] and score < difficulty_markers[1]:
        chosen_question = get_question(difficulty_markers[0],
                                          difficulty_markers[1])
    elif score >= difficulty_markers[1] and score < difficulty_markers[2]:
        chosen_question = get_question(difficulty_markers[1],
                                          difficulty_markers[2])
    else:
        chosen_question = get_question(difficulty_markers[2],
                                          len(questions))
    return chosen_question


def get_quiz_field_values(user):
    chosen_question = choose_question(user["score"])
    
    # Get the 4 choices to present to user
    option_copy = chosen_question.options.copy()
    presented_options = []
    presented_options.append(chosen_question.answer)
    
    # Choose 3 random options
    for _ in range(3):
        index = random.choice(range(0, len(option_copy)))
        presented_options.append(option_copy[index])
        del option_copy[index]
    
    # Randomize the 3 options with the answer
    random.shuffle(presented_options)
    return chosen_question, presented_options


# Waits for user to send an answer #Currently using timer in main.js
def await_answer(user):
    print("awaiting answer")
    start_time = time.time()
    while True:
        if user.kill_thread:
            print("killed")
            user.question = None
            break

        if time.time() - start_time > 45:
            print("timed out")
            user.question = None
            user.score -= 1
            break

        if closed:
            break

# Methods to be called by client

# Displays the main home page
@app.route('/')
def home():
    #check if logged in
    if(not('name' in session.keys())):
        return redirect(url_for("login"))
    else:
        return render_template('index.html')

# Send the next question to the proper user
@app.route('/send', methods=['POST'])
def send():
    # Get a question and possible answer list
    question, options_list = get_quiz_field_values(session["data"])

    # Create tie between question and user
    #current_question = CurrentQuestion(session["data"]["username"], question)
    #current_questions.append(current_question)
    #Rework
    try:
        user = activeUsers[session["data"]["username"]]
    except:
        #If user rejoins from session
        activeUsers[session["data"]["username"]] =  User(session["data"]["username"])
        user = activeUsers[session["data"]["username"]]
    user.question = question

    # Start thread to determine when to auto-fail question
    #user.thread = threading.Thread(target=await_answer, args=[user])
    #user.thread.start()
    
    return json.dumps({
        'prompt': question.question,
        'ans1': options_list[0],
        'ans2': options_list[1],
        'ans3': options_list[2],
        'ans4': options_list[3]
    })

# Receive the answer provided by user
@app.route('/receive', methods=["POST"])
def receive():
    # Find correct user in list
    try:
        user = activeUsers[session["data"]["username"]]
    except:
        #If user rejoins from session
        activeUsers[session["data"]["username"]] =  User(session["data"]["username"])
        user = activeUsers[session["data"]["username"]]
    # Find active question for user

    #user_question = find_current_question(session["data"])

    print(f'\n{user.question}\n{str(request.form.get("answer-choice"))}')

    if user.question is None:
        print('error, user_question is none\n')
        return ''
    
    

    # Determine if score needs to increase or decrease
    if (user.question.answer == request.form.get('answer-choice')):
        print("correct")
        user.score += 1
        dataDict = {}
        dataDict["prompt"] = user.question.question
        dataDict["cat"] = user.question.catergory
        dataDict["length"] = 0
        dataDict["correct"] = True
        user.questionData.append(dataDict)
    elif not closed:
        print("incorrect")
        dataDict = {}
        dataDict["prompt"] = user.question.question
        dataDict["cat"] = user.question.catergory
        dataDict["length"] = 0
        dataDict["correct"] = False
        user.questionData.append(dataDict)
        user.score -= 1
    
    # Kill user's thread and join to receive
    #user.kill_thread = True
    #user.thread.join()
    return ''

#LOGIN PAGE login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        #Check if matches the database
        cursor.execute('select * from users WHERE username="'+username+'"')
        result = cursor.fetchall()
        if(len((result))==0):
            error = "User Does Not Exist"
            return render_template('login.html', error=error)
        elif(password != result[0][2]):
            error = "Password is incorrect"
            return render_template('login.html', error=error)
        else:
            #Sessioning for users
            session.permanent = True
            session["name"] = username
            userDict = {}
            userDict['username'] = username
            userDict['score'] = 0
            userDict['timer'] = None
            session["data"] = userDict
            activeUsers[username] = User(username)
            return redirect(url_for("home"))
            #bring to homepage

    return render_template('login.html', error=error)

#Register Page register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        cursor.execute('select * from users WHERE username="'+username+'"')
        result = cursor.fetchall()
        if(len((result))>0):
            error = "Username Already Exists"
            return render_template('register.html', error=error)
        else:
            #need to hash the password and check requirements
            cursor.execute('INSERT INTO users VALUES ("'+email+'", "'+username+'", "'+password+'", 0);')
            conn.commit()
            return redirect(url_for("login"))
        print(username)
        print(password)
        #Check if matches the database
        
    return render_template('register.html', error=error)
@app.route("/logout")
def logout():
    session.pop("name", None)
    return redirect("/")

if __name__ == '__main__':
    login_database()
    get_questions()
    save_thread = threading.Thread(target=save_users_on_timer)
    save_thread.start()
    #database
    
    # app.run(debug = False, host = '10.0.0.69', port = 5000)
    app.run(debug=False, port=5000)
    # Will only reach this point on the app being closed or interrupted
    print('\nProgram will end after next scheduled save.')
    print('NOTE: No new user activity will be recorded at this time.')
    closed = True
    for question in current_questions:
        question.user.timer_thread.join()
    save_thread.join()
    conn.close() #Close database connection
    print('Program ended by KeyboardInterrupt.\n')
    sys.exit(0)