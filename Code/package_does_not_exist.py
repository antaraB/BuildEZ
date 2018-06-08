#!/usr/bin/env python
'''
ERROR: package <package-name> does not exist

Eg: /home/travis/build/junkdog/artemis-odb/artemis/src/main/java/com/artemis/io/SaveFileFormat.java:[7,47] package com.sun.xml.internal.ws.api.wsdl.parser does not exist

Will rewrite the file to remove the imported package
'''
import re
from __future__ import print_function

regex_package_not_found = r"(package [\w.]+ does not exist)"
regex_full_error = r"((\/([\w-]+))+\.java):\[(\d+),\d+\] package ([\w\.]+) does not exist" 

# extract info from the grep error file
def get_info_from_error_file (grep_error_filepath, to_print):
    with open(grep_error_filepath) as grep_error_file:
        for line in grep_error_file:
            if re.search(regex_package_not_found,line):
                filepath, _, filename, line_num, required_package_name = re.search(regex_full_error,line).groups()
                break
    if to_print:
        print("get_info_from_error_file: filepath: ",filepath, "package:", required_package_name, "line num:",line_num)
    return filepath, required_package_name, line_num

# extract info from the grep error string
def get_info_from_error_message (grep_error_string, to_print):
    if re.search(regex_package_not_found,grep_error_string):
        filepath, _, filename, line_num, required_package_name = re.search(regex_full_error,line).groups()
        return filepath, required_package_name, line_num
    if to_print:
        print("get_info_from_error_message: filepath: ",filepath, "package:", required_package_name, "line num:",line_num)
    return None,None,None

def fix_error_package_dne (errorfilepath, required_package_name, line_num=None, to_print):
    new_file=[]
    regex_import_error = r"import "+required_package_name+r";"
    # open error file, read, make the fix, write the file
    with open (errorfilepath) as error_file:
        for line in error_file:
            # test run: if line nums match 
            if re.match(regex_import_error,line): #or (line_num and error_file.index(line) == (line_num)):
                if to_print:
                    print("fix_error_package_dne: skipped line : ",line)
                continue # don't add that line to new_file
            else :
                new_file.append(line)
    if to_print:
        print("fix_error_package_dne: Finished reading file  : ",errorfilepath)
    with open (errorfilepath) as error_file
        error_file.write(new_file)
        if to_print:
            print("fix_error_package_dne: Finished writing file  : ",errorfilepath)
        error_file.close()
        return 0
    return -1 #error - didn't open file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('grep_error',action='store', help="Complete path of grepped error file")
    parser.add_argument('-s','--error-message', action='store_true', help="if main argument is string ")
    parser.add_argument('-v','--verbose', action='store_true', help=" Will print values at intermediate steps ")
    
    args = parser.parse_args()
    grep_error = args.grep_error
    is_string = args.error-message
    to_print = args.verbose

    if is_string:
        filepath, package-name, line_num = get_info_from_error_message(grep_error, to_print)
    else :
        filepath, package-name, line_num = get_info_from_error_file(grep_error, to_print)

    if filepath and package-name:
        if fix_error_package_dne(filepath, package-name, line_num, to_print)!=0:
            print("File not written")

if __name__=="__main__":
    main()










