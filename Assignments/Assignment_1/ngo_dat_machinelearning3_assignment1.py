
# Task 1: Input file name
import pandas as pd

BASE_DATA_FOLDER = f'data-files\\Data_Files'

class_file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")

try:        
    class_df = pd.read_csv(f'{BASE_DATA_FOLDER}\\{class_file_name}.txt', index_col=0, header=None)
    print(f'Successfully opened {class_file_name}.txt')
except IOError:
    print('File cannot be found.')

# Task 2: Validate data

from enum import Enum
import re

REQUIRED_ANSWER = 25

errors = []
valid_df = pd.DataFrame(columns = class_df.columns)

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

for index, row in class_df.iterrows():
    
    if(len(row) != REQUIRED_ANSWER):
        error = DataError(
            type = ErrorType.WRONG_ANSWER_AMOUNT,
            message = f'Invalid line of data: does not contain exactly {REQUIRED_ANSWER + 1} values:',
            data = row,
        )
        error.print()
        errors.append(error)
        continue
    
    student_id = index
    
    if(not re.match(r'^N\d{8}$', student_id)):
        error = DataError(
            type = ErrorType.ID_INVALID,
            message = f'Invalid line of data: N# is invalid',
            data = row,
        )
        error.print()
        errors.append(error)
        continue
    
    valid_df.loc[index] = row
        
print('\n**** REPORT ****\n')

print(f'Total valid lines of data: {len(class_df) - len(errors)}')

print(f'Total invalid lines of data: {len(errors)} \n')

# Task 3: Calculate
import numpy as np

ANSWER_KEYS = pd.Series(("B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D").split(','))

student_scores = []

for index, row in valid_df.iterrows():
    student_id = index
    student_answers = row
    student_score = 0
    
    for i, answer in student_answers.items():
        if(pd.notna(answer) == False):
            continue
        elif(answer == ANSWER_KEYS[i-1]):
            temp = ANSWER_KEYS[i-1]
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

# Task 4: Save Result

df = pd.DataFrame(student_scores)
df.to_csv(f'results/{class_file_name}_grades.txt', index=False, header=False)