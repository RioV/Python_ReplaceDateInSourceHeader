import subprocess
import os
import re
import sys


# Function define
def get_file_content(file_name):
    print('get_file_content - file_name = ' + file_name)
    file_to_open = open(file_name, 'r')

    file_content_to_be_read = file_to_open.read().splitlines()
    count = 0
    for line_content in file_content_to_be_read:
        count += 1
        # print('Line = ' + line_content)
        new_content = check_file_content_is_ok_to_be_replace(line_content)
        if new_content != line_content:
            print(new_content)
            replace(file_content_to_be_read, line_content, new_content)
        if count > 15:
            break

    file_to_open.close()
    file_to_save = open(file_name, 'w')
    file_to_save.write("\n".join(file_content_to_be_read))
    file_to_save.close()


def replace(l, X, Y):
    for i,v in enumerate(l):
        if v == X:
            l.pop(i)
            l.insert(i, Y)


def check_file_content_is_ok_to_be_replace (content_tobe_replace):
    # Check first 10 line
    return_value = content_tobe_replace
    temp_value = content_tobe_replace.strip()

    is_this_line_comment = False
    is_this_line_have_date_time = False

    two_first_character = temp_value[:2]
    # print (two_first_character)
    if two_first_character == '//':
        is_this_line_comment = True

    if '.' in temp_value:
        x_last_character = temp_value[-9:]
        x_last_character = x_last_character.replace('.', '')
    else:
        x_last_character = temp_value[-8:]
    # print(x_last_character)

    if re.match('\d\d/\d\d\/\d\d', x_last_character):
        # print("it matches!")
        is_this_line_have_date_time = True
        if '.' in return_value:
            return_value = return_value[:-2]
            return_value += '6.'
        else :
            return_value = return_value[:-1]
            return_value += '6'

    if is_this_line_comment and is_this_line_have_date_time:
        return return_value
    else:
        return content_tobe_replace

# Implement start
# File that diff between 2 version will be saved
fileDiff = 'diffFromPython.txt'

# Get version to be compare from command line
list_command = sys.argv

if len(list_command) == 3:
    print (list_command)
    first_version = list_command[1]
    last_version = list_command[2]

    # Running git command diff
    pr = subprocess.Popen(('/usr/bin/git diff --name-only {0} {1} > {2}').format(first_version, last_version, fileDiff),
                          cwd=os.path.dirname(os.getcwd() + '/'),
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pr.communicate()

    fileListChangedGit = open(os.path.dirname(os.getcwd() + '/') + '/' + fileDiff, 'r')
    # Get list of changed file
    listFileThatToBeExecute = [];
    for changedFile in fileListChangedGit:
        changedFile = changedFile.strip()
        extension = changedFile[-2:]
        if extension == '.h' or extension == '.m':
            listFileThatToBeExecute.append(changedFile)

    for file_name in listFileThatToBeExecute:
        get_file_content(os.getcwd() + '/' + file_name)

    os.remove(fileDiff)
else:
    print ('Viet an shit')
