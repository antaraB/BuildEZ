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
regex_till_package_not_found = r"(.)+ package [\w.]+ does not exist"
regex_filename = r"((\/([\w+-]+))+.java):(\[(\d+),(\d+)\])" #gets the java file which needs to be edited
# group1 is file name (with path), group 3 is just filename (no java). group 5 is line num, group 6 is col num.
with open(GREP_ERROR) as grep_error_file:
	grep_error_file.read()



