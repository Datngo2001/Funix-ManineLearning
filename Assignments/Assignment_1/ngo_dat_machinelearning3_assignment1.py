
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
        
print('\n**** REPORT ****\n')

print(f'Total valid lines of data: {len(rows) - len(errors)}')

print(f'Total invalid lines of data: {len(errors)}')


