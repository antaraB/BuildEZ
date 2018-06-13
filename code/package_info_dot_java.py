#!/usr/bin/env python
from __future__ import print_function
import re
import os
import subprocess
import fileinput

#input_error = "com.adobe.acs.commons.email: Version increase required; detected 1.1.0, suggested 1.2.0"

#STORING PATH TO ALL PACKAGE-INFO.JAVA FILES IN AN ARRAY
def find_all_package_info_java_files(name, path, to_print=False):
    if to_print:
        print ("--------------Inside find_all_package_info_java_files------------")   
    packageinfo = []
    for root, dirs, files in os.walk(path):
        if name in files:
            packageinfo.append(os.path.join(root, name))
    return packageinfo

#SELECTING PATHS THAT END WOTH PATH MENTIONED IN ERROR MESSAGE
def find_specific_path(patharray, input_error, to_print=False):
    if to_print:
        print ("--------------Inside find_specific_path------------")
    subpath = re.search(r"([\w\.]+): Version .+ required\; detected ([\d\.]+), suggested ([\d\.]+)", input_error).groups()[0]
    subpath = re.sub(r"\.",r"/", subpath)
    old_version = re.search(r"([\w\.]+): Version .+ required\; detected ([\d\.]+), suggested ([\d\.]+)", input_error).groups()[1]
    new_version = re.search(r"([\w\.]+): Version .+ required\; detected ([\d\.]+), suggested ([\d\.]+)", input_error).groups()[2]
    if to_print:
        print ("Sub path: ",subpath," | Old Version: ", old_version," | New Version: ", new_version)
    for filepath in patharray:
        if subpath in filepath:
            with open('%s' % filepath, 'r') as filename:
                newfile = []
                for line in filename:
                    if old_version in line:
                        if to_print:
                            print ("To replace: ", line)
                        line = line.replace(old_version, new_version)
                    newfile.append(line)
                filename.close()
                
            with open('%s' % filepath, 'w') as filename:
                for line in newfile:
                    filename.write(line)
                    

#MAIN FUNCTION
def main(input_error, to_print=False):
    if to_print:
        print ("---------INSIDE MAIN (package_info_dot_java)------------")
    name = "package-info.java"
    path = "/home/travis/build/failed"
    packageinfo = find_all_package_info_java_files(name, path, to_print)
    find_specific_path(packageinfo, input_error, to_print)

if __name__=="__main__":
    main(input_error)

                    

