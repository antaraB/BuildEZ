#!/usr/bin/env python
from __future__ import print_function
import subprocess
import re
import argparse

from package_does_not_exist import get_info_from_error_message, fix_error_package_dne, modify_to_failed
import package_info_dot_java
import snapshot_xml

import check_build

import could_not_resolve_dependencies
import remove_plugin
import parent_update_version


def main(to_print=False, to_print_build=False):
    # save a copy of the original
    subprocess.call(['cp','-r','/home/travis/build/failed/','/home/travis/build/failed_original/'])
    # change permissions for diffandgrep
    subprocess.call(['chmod','+x','../scripts/diffandgrep.sh'])
    #generate grep-file
    subprocess.call('../scripts/diffandgrep.sh')
    build_pass = False # whether build has passed or not
    build_message = None # any message you want to print with build passed (usually error name/ brief summary)
    
    try:
        with open('/home/travis/grep_errors.txt') as grep_error_file:
            for line in grep_error_file.readlines():

                # ERROR: package <package-name> does not exist
                filepath, package_name, line_num = get_info_from_error_message(line, to_print)
                if filepath and package_name:
                    if fix_error_package_dne(modify_to_failed(filepath), package_name, line_num, to_print)>0: #Fix worked as expected
                        if check_build.main(to_print_build): #Build Passed!
                            build_pass = True
                            build_message = "Fixed package-does-not-exist error by removing "+package_name+" import statement from "+modify_to_failed(filepath)
                            break
                    else : # Error wasn't fixed
                        if to_print:
                            print("\nTried package-does-not-exist, no error detected and no changes made to build")

                # ERROR: Version required and detected don't match
                if re.search(r"([\w\.]+): Version .+ required\; detected ([\d\.]+), suggested ([\d\.]+)", line):
                    package_info_dot_java.main(line, to_print)
                    if check_build.main(to_print_build): #Build Passed!
                        build_pass = True
                        build_message = "Fixed the error by changing version in package-info.java"
                        break
                    else : # Error wasn't fixed
                        if to_print:
                            print("\nFailed to fix build error by using version change in package-info.java")

                # ERROR: Failed to collect dependencies at XXX-SNAPSHOT
                if re.search(r"Failed to collect dependencies at [\w\.\-]+:[\w\-]+:jar:[\d\.]+-SNAPSHOT", line):
                    errors = re.search(r"(Failed to collect dependencies at [\w\.\-]+:[\w\-]+:jar:[\d\.]+-SNAPSHOT)", line).groups()[0]
                    snapshot_xml.main(errors, to_print)
                    if check_build.main(to_print_build): #Build Passed!
                        build_pass = True
                        build_message = "Fixed the error by removing SNAPSHOT from version in pom.xml"
                        break
                    else : # Error wasn't fixed
                        if to_print:
                            print("\nFailed to fix build error")

                if re.search(r".+ (Could not find artifact ([\w\.\:]+) at specified path ((\/([\w\.+-]+))+)+)", line) or re.search(r".+ (Could not find artifact ([\w\.\:]+) ([\w\.+-]+))", line):
                    could_not_resolve_dependencies.main(line, to_print)
                    if check_build.main(to_print_build): #Build Passed!
                        build_pass = True
                        build_message = "Fixed the error by resolving the missing dependency"
                        break
                    else : # Error wasn't fixed
                        if to_print:
                            print("\nFailed to fix build error updating the dependency path")

                if re.search(r".+ Plugin ([\w\.\:\-]+) or one of its dependencies could not be resolved.+ (Could not find artifact ([\w\.\:\-]+))",line):
                    remove_plugin.main(line, to_print)
                    if check_build.main(to_print_build): #Build Passed!
                        build_pass = True
                        build_message = "Fixed the error by removing the errerons plugin"
                        break
                    else : # Error wasn't fixed
                        if to_print:
                            print("\nFailed to fix build error by removing the plugin")

                if re.search(r"", line):
                    parent_update_version.main(line, to_print)
                    if check_build.main(to_print_build): #Build Passed!
                        build_pass = True
                        build_message = "Fixed the error by removing the errerons plugin"
                        break
                    else : # Error wasn't fixed
                        if to_print:
                            print("\nFailed to fix build error by updating the version for the artifact of the parent")


    except IOError as e: # couldn't open grep_errors.txt
        if to_print:
            print("Couldn't open grep_errors.txt to read (%s)." % e)
        return -1 # couldn't open file
    
    if build_pass:
        print("Build passed : ", build_message)
        return 1
    else :
        print("Build failed: Error couldn't be fixed using the defined dependency-error fixes")
        # delete working copy
        subprocess.call(['rm','-r','/home/travis/build/failed/'])
        # rename original copy to failed
        subprocess.call(['mv','/home/travis/build/failed_original/','/home/travis/build/failed/'])
        return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose', action='store_true', default=False, help=" Will print values at intermediate steps ")
    parser.add_argument('-b','--build-output', action='store_true', default=False, help=" Will not suppress output from build ")
    args = parser.parse_args()
    to_print = args.verbose
    to_print_build = args.build_output
    if to_print:
        print("Verbose option is enabled")
    if to_print_build:
        print("Verbose option for build message is enabled")
    main(to_print, to_print_build)