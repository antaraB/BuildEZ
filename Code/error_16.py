#assuming we've detected that it's this error
# error: package X not detected
# /home/travis/build/junkdog/artemis-odb/artemis/src/main/java/com/artemis/io/SaveFileFormat.java:[7,47] package com.sun.xml.internal.ws.api.wsdl.parser does not exist
'''
PROCEDURE
read failed log 
separate grep errors?


'''


import re

FAILED_LOG = ""
GREP_ERROR = ""
required_package_name = None
regex_package_not_found = r"(package [\w.]+ does not exist)"
regex_till_package_not_found = r".+ package ([\w\.]+) does not exist"
regex_filename = r"((\/([\w-]+))+\.java):(\[(\d+),(\d+)\])" #gets the java file which needs to be edited
# group1 is file name (with path), group 3 is just filename (no java). group 5 is line num, group 6 is col num.
regex_full = r"((\/([\w-]+))+\.java):\[(\d+),\d+\] package ([\w\.]+) does not exist"

# extract info from grep-ped error file
with open(GREP_ERROR) as grep_error_file:
    for line in grep_error_file:
        if re.search(regex_package_not_found,line):
            # filepath, _, filename, _, line_num, _ = re.search(regex_filename,line).groups()
            filepath, _, filename, line_num, required_package_name = re.search(regex_full,line).groups()
            break

new_file=[]
regex_import_error = r"import "+required_package_name+";"
# open error file, read, make the fix, write the file
with open (filepath) as error_file:
    for line in error_file:
        # test run: if line nums match 
        if error_file.index(line) == (line_num) and re.match(regex_import_error,line):
            continue #don't add that line to new_file
        else :
        new_file.append(line)












