
# Task 1: Input file name


BASE_DATA_FOLDER = f'data-files\\Data_Files'

class_file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
file_content = ''

try:
    with open(f'{BASE_DATA_FOLDER}\\{class_file_name}.txt', 'r') as file:
        file_content = file.read()
    print(f'Successfully opened {class_file_name}.txt')
except IOError:
    print('File cannot be found.')

# Task 2: Validate data

from enum import Enum
import re

REQUIRED_ANSWER = 25

errors = []
valid_rows = []

class ErrorType(Enum):
    ID_INVALID = 1
    WRONG_ANSWER_AMOUNT = 2
    
class DataError:
    def __init__(self, type: ErrorType, message: str, data: str):
        self.type = type
        self.message = message
        self.data = data
    
    def print(self):
        print(self.message)
        print(self.data + '\n')
        

print('\n**** ANALYZING ****\n')

rows = file_content.split('\n')

for row in rows:
    columns = row.split(',')
    
    if(len(columns) != REQUIRED_ANSWER + 1 ):
        
        error = DataError(
            type = ErrorType.WRONG_ANSWER_AMOUNT,
            message = f'Invalid line of data: does not contain exactly {REQUIRED_ANSWER + 1} values:',
            data = row,
        )
        
        error.print()
        errors.append(error)
        
        continue
    
    student_id = columns[0]
    
    if(not re.match(r'^N\d{8}$', student_id)):
        error = DataError(
            type = ErrorType.ID_INVALID,
            message = f'Invalid line of data: N# is invalid',
            data = row,
        )
        
        error.print()
        errors.append(error)
        
        continue
    
    valid_rows.append(row)
        
print('\n**** REPORT ****\n')

print(f'Total valid lines of data: {len(rows) - len(errors)}')

print(f'Total invalid lines of data: {len(errors)}')

# Task 3: Calculate
import numpy as np

ANSWER_KEYS = ("B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D").split(',')

student_scores = []

for row in valid_rows:
    row_split = str(row).split(',')
    student_id = row_split[0]
    student_answers = row_split[1:]
    student_score = 0
    
    for i in range(0, len(student_answers) - 1):
        if(len(student_answers[i]) == 0):
            continue
        elif(student_answers[i] == ANSWER_KEYS[i]):
            student_score += 4
        else:
            student_score += -1
            
    student_scores.append([student_id, student_score])

student_scores = np.array(student_scores)

scores = student_scores[:,1].astype(dtype=int)

print(f'Mean (average) score: {scores.mean()}')
print(f'Highest score: {scores.max()}')
print(f'Lowest score: {scores.min()}')
print(f'Range of scores: {scores.max() - scores.min()}')
print(f'Median score: {np.median(scores)}')
