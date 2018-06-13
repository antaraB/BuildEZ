#!/usr/bin/env python

from __future__ import print_function
import re
import argparse
'''
ERROR: package <package-name> does not exist

Eg: /home/travis/build/junkdog/artemis-odb/artemis/src/main/java/com/artemis/io/SaveFileFormat.java:[7,47] package com.sun.xml.internal.ws.api.wsdl.parser does not exist

Will rewrite the file to remove the imported package
'''

regex_package_not_found = r"(package [\w.]+ does not exist)"
regex_full_error = r"((\/([\w-]+))+\.java):\[(\d+),\d+\] package ([\w\.]+) does not exist" 
# regex_full_error_import =r"((\/([\w-]+))+\.java):\[(\d+),\d+\] \(imports\) UnusedImports: Unused import - ([\w\.]+)\."

# extract info from the grep error file
def get_info_from_error_file (grep_error_filepath, to_print=False):
    with open(grep_error_filepath) as grep_error_file:
        for line in grep_error_file:
            if re.search(regex_package_not_found,line):
                filepath, _, filename, line_num, required_package_name = re.search(regex_full_error,line).groups()
                if to_print:
                    print("get_info_from_error_file: filepath: ",filepath, "package:", required_package_name, "line num:",line_num)
                return filepath, required_package_name, line_num
    return None,None,None
    

# extract info from the grep error string
def get_info_from_error_message (grep_error_string, to_print=False):
    if re.search(regex_package_not_found,grep_error_string):
        filepath, _, filename, line_num, required_package_name = re.search(regex_full_error,grep_error_string).groups()
        if to_print:
            print("get_info_from_error_message: filepath: ",filepath, "package:", required_package_name, "line num:",line_num)
        return filepath, required_package_name, line_num
    return None,None,None

def fix_error_package_dne (errorfilepath, required_package_name, line_num=None, to_print=False):
    new_file=[]
    lines_skipped = 0 
    # open error file, read, make the fix, write the file
    try:
        with open(errorfilepath) as error_file:
            ctr=0
            for line in error_file:
                ctr+=1
                # print (required_package_name in line,line_num,ctr,line)
                if required_package_name in line and ctr==int(line_num): 
                    lines_skipped+=1
                    if to_print:
                        print("fix_error_package_dne: skipped line : ",line)
                    continue # don't add that line to new_file
                else :
                    new_file.append(line)
            if to_print:
                print("fix_error_package_dne: Finished reading file  : ",errorfilepath)
            error_file.close()
    except IOError as e:
        if to_print:
            print("fix_error_package_dne: Couldn't open file to read (%s)." % e)
        return -1 # couldn't open file

    if lines_skipped == 0:
        if to_print:
            print("fix_error_package_dne: No lines altered in ",errorfilepath)
        return -2 #no errors found

    try:   
        with open(errorfilepath, 'w') as error_file:
            for line in new_file:
                error_file.write(line)
            if to_print:
                print("fix_error_package_dne: Finished modifying file  : ",errorfilepath," : ",lines_skipped," lines skipped")
            error_file.close()
            return lines_skipped
    except IOError as e:
        if to_print:
            print("fix_error_package_dne: Couldn't open file to write (%s)." % e)
        return -1 # couldn't open file
    return -3 #other random error (not zero because it's confusing)

def modify_to_failed (filepath):
    filepath = re.sub(r"(\/home\/travis\/build)((\/([\w-]+))+\.java)", r"\1/failed\2", filepath)
    return filepath

def main(grep_error, is_string, to_print=False):
    if is_string:
        filepath, package_name, line_num = get_info_from_error_message(grep_error, to_print)
    else :
        filepath, package_name, line_num = get_info_from_error_file(grep_error, to_print)

    if filepath and package_name:
        if fix_error_package_dne(modify_to_failed(filepath), package_name, line_num, to_print)<=0:
            print("File not fixed")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('grep-error',action='store', help="Complete path of grepped error file")
    parser.add_argument('-s','--error-message', action='store_true', default=False, help="if main argument is string ")
    parser.add_argument('-v','--verbose', action='store_true', default=False, help=" Will print values at intermediate steps ")
    
    args = parser.parse_args()
    grep_error = args.grep_error
    is_string = args.error_message
    to_print = args.verbose
    main(grep_error, is_string, to_print)