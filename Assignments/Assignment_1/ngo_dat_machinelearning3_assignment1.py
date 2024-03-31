BASE_DATA_FOLDER = f'data-files\\Data_Files'

class_file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")

try:
    with open(f'{BASE_DATA_FOLDER}\\{class_file_name}.txt', 'r') as file:
        content = file.read()
    print(f'Successfully opened {class_file_name}.txt')
except IOError:
    print('File cannot be found.')
