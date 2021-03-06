#!/usr/bin/env python
from __future__ import print_function
import subprocess
import argparse
try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def main(to_print=False):
    if to_print:
        result = subprocess.call('/usr/local/bin/run_failed.sh')
    else :  
        result = subprocess.call('/usr/local/bin/run_failed.sh', stdout=DEVNULL, stderr=subprocess.STDOUT)
    if result == 0:
        if to_print:
            print("Build Passed")
        return True
    else:
        if to_print:
            print("Build Failed")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose', action='store_true', default=False, help=" Will not suppress output from build")
    args = parser.parse_args()
    to_print = args.verbose
    main(to_print)