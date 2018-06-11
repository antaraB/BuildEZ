#!/usr/bin/env python
from __future__ import print_function
import re
import argparse
from package_does_not_exist import get_info_from_error_message, fix_error_package_dne, modify_to_failed
import check_build


def main(to_print):
	subprocess.call('./scripts/diffandgrep.sh')
	build_pass = False # whether build has passed or not
	build_message = None # any message you want to print with build passed (usually error name/ brief summary)
	try:
		with open('grep_errors.txt') as grep_error_file:
			for line in grep_error_file.read():

				# ERROR: package <package-name> does not exist
				filepath, package_name, line_num = get_info_from_error_message(grep_error, to_print)
				if filepath and package_name:
					if fix_error_package_dne(modify_to_failed(filepath), package_name, line_num, to_print)>0: #Fix worked as expected
			            if check_build.main(to_print): #Build Passed!
			            	build_pass = True
			            	build_message = "Fixed package-does-not-exist error by removing "+package_name+" import statement from "+modify_to_failed(filepath)
			            	break
					else : # Error wasn't fixed
						if to_print:
							print("Tried package-does-not-exist, no error detected and no changes made to build")

				# ADD OTHER ERRORS HERE

	except IOError as e: # couldn't open grep_errors.txt
        if to_print:
            print("Couldn't open grep_errors.txt to read (%s)." % e)
        return -1 # couldn't open file
	
	if build_pass:
		print("Build passed : ", build_message)
		return 1
	else :
		print("Build failed: Error couldn't be fixed using the defined dependency-error fixes")
		return -1


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
    parser.add_argument('grep_error',action='store', help="Complete path of grepped error file")
    parser.add_argument('-s','--error_message', action='store_true', default=False, help="if main argument is string ")
    parser.add_argument('-v','--verbose', action='store_true', default=False, help=" Will print values at intermediate steps ")
    args = parser.parse_args()
    grep_error = args.grep_error
    is_string = args.error_message
    to_print = args.verbose
	main()