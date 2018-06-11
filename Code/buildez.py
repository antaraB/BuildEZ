#!/usr/bin/env python
from __future__ import print_function
import re
import argparse
from package_does_not_exist import get_info_from_error_message, fix_error_package_dne
import check_build


def main(to_print):
	subprocess.call('./scripts/diffandgrep.sh')
	build_pass = False
	with open('grep_errors.txt') as grep_error_file:
		for line in grep_error_file.read():

			# ERROR: package <package-name> does not exist
			filepath, required_package_name, line_num = get_info_from_error_message(line, to_print)
			if filepath and required_package_name:
				if fix_error_package_dne(modify_to_failed(filepath), package_name, line_num, to_print)>0:
		            if check_build.main(to_print): #Build Passed!
		            	build_pass = True
		            	break
				else : # Error wasn't fixed
					if to_print:
						print("Tried package-does-not-exist, no error detected and no changes made to build")








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