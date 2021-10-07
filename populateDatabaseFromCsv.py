import mysql.connector

import csv, random, re, os
from itertools import islice
import threading, time, json, sys

conn = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='mysql')
closed = False # Flag for save_thread
save_thread = None # Contains the thread saving user information on interval
questions = [] # Holds Question objects
options = [] # Determines all the columns that contain options for answers
difficulty_markers = [] # Marks where the first question in a given difficulty is
users = [] # Stores users here until db is up and running
current_questions = [] # Ties users to their current questions and deletes after

class Question:
    def __init__(self, question, answer, options,catergory,difficulty):
        self.question = question # The prompt
        self.answer = answer # The correct answer
        self.options = options # Array with all options to choose from
        self.catergory = catergory
        self.difficulty = difficulty

def read_file():
    with open('Questions_1.csv', newline = '') as csv_file:
        # Open csv and split into nested arrays
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        first_row = next(csv_reader) # Need to check separately

        answer_index = None
        random_index = None # Used to detect changes in questions with variants
        category_index = None
        # Get all the option columns and the answer index
        index = 0
        for cell in first_row:
            if cell.__contains__('Option'):
                options.append(index)
            elif cell.__contains__('Correct Answer'):
                answer_index = index
            elif cell.__contains__('Type'):
                category_index = index
            elif cell.__contains__('Difficulty (1-10)'):
                difficulty_index = index
            index += 1

        for row in csv_reader: # Check each row in split CSV file
            try:
                # Skips current row from being added to questions
                if row[0] == '':
                    continue

                # Checks where difficulty begins
                if row[0].__contains__('Assigned Difficulty:'):
                    difficulty_markers.append(len(questions))
                    continue
                
                # Checking question
                row[0], random_index = check_for_variant(row[0], random_index,
                    r"\{([A-Za-z0-9_\/]+)\}") 
                if random_index is not None: 
                    # If question changed, answer needs to change too
                    row[answer_index], random_index = check_for_variant(
                        row[answer_index], random_index, r"\{([A-Za-z0-9_\.\;\(\)\/]+)\}")
                    random_index = None

                # Gets options from option columns for given question
                answer_options = []
                for index in options:
                    if row[index] != '':
                        answer_options.append(row[index])
                
                # Append question to list
                questions.append(Question(row[0], row[answer_index], answer_options,row[category_index],row[difficulty_index]))

            except IndexError:
                print('List Complete\n')
def check_for_variant(cell, index, regex):
    if cell.__contains__('{'):

        question_choice = re.search(regex, cell) 
        question_choice_string = question_choice.group(1)
        question_choice_split = question_choice_string.split('/')

        random_variant = None
        if index is None:
            random_variant = random.choice(question_choice_split)
            index = question_choice_split.index(random_variant)
        else:
            random_variant = question_choice_split[index]
        cell = cell.replace(question_choice_string, random_variant)
        cell = cell.replace('{', '')
        cell = cell.replace('}', '')
    return cell, index   
read_file()


mycursor = conn.cursor()

for question in questions:
    print('INSERT INTO question VALUES ("'+question.question+'", "'+question.options[0]+'", "'+question.options[1]+'", "'+question.options[2]+'",  "'+question.options[3]+'",  "'+question.options[4]+'","'+question.options[5]+'", "'+question.answer+'", "'+question.catergory+'",'+question.difficulty+');')
    mycursor.execute('INSERT INTO question VALUES ("'+question.question+'", "'+question.options[0]+'", "'+question.options[1]+'", "'+question.options[2]+'",  "'+question.options[3]+'",  "'+question.options[4]+'","'+question.options[5]+'", "'+question.answer+'", "'+question.catergory+'",'+question.difficulty+');')
    conn.commit()