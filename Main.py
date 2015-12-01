import subprocess
import os
import re
import sys


# Function define
def get_file_content(file_name):
    file_to_open = open(file_name, 'r')

    file_content_to_be_read = file_to_open.read().splitlines()
    count = 0
    for line_content in file_content_to_be_read:
        count += 1
        new_content = check_file_content_is_ok_to_be_replace(line_content)
        if new_content != line_content:
            print ('Update content from')
            print(line_content)
            print ('to')
            print(new_content)
            print('\n')
            replace(file_content_to_be_read, line_content, new_content)
        if count > 10:
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
    # temp_value = content_tobe_replace.strip()
    temp_value = content_tobe_replace
    # print('Line value to be process = {}'.format(temp_value))

    is_this_line_comment = False
    is_this_line_have_date_time = False

    two_first_character = temp_value[:2]
    if two_first_character == ' *':
        # print('Map two first chars')
        is_this_line_comment = True

    # Get year from comment line
    # Check for year with format 2013-2015
    if len(re.findall('\d\d\d\d-\d\d\d\d', temp_value)) == 1:
        founded_value = re.findall('\d\d\d\d-\d\d\d\d', temp_value)[0]
        is_this_line_have_date_time = True
    elif len(re.findall('\d\d\d\d - \d\d\d\d', temp_value)) == 1:
        founded_value = re.findall('\d\d\d\d - \d\d\d\d', temp_value)[0]
        is_this_line_have_date_time = True
    elif len(re.findall('\d\d\d\d', temp_value)) == 1:
        founded_value = re.findall('\d\d\d\d', temp_value)[0]
        is_this_line_have_date_time = True
    else:
        return temp_value

    replace_value = founded_value[:-1]
    replace_value += '6'

    return_value = return_value.replace(founded_value, replace_value)

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
    first_version = list_command[1]
    last_version = list_command[2]

    # Running git command diff
    pr = subprocess.Popen(('/usr/bin/git diff --name-only {0} {1} > {2}').format(first_version, last_version, fileDiff),
                          cwd=os.path.dirname(os.getcwd() + '/'),
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pr.communicate()

    fileListChangedGit = open(os.path.dirname(os.getcwd() + '/') + '/' + fileDiff, 'r')
    if fileListChangedGit:
        print ('Have list file changed')
    # Get list of changed file
    listFileThatToBeExecute = [];
    for changedFile in fileListChangedGit:
        changedFile = changedFile.strip()
        extension = changedFile[-2:]
        if extension == '.h' or extension == '.m':
            listFileThatToBeExecute.append(changedFile)

    print('Number of file to be execute = {}'.format((len(listFileThatToBeExecute))))
    print ('\n')
    for file_name in listFileThatToBeExecute:
        print('File = ' + file_name)
        get_file_content(os.getcwd() + '/' + file_name)

    os.remove(fileDiff)
else:
    print ('Viet an shit')
