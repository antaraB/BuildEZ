import re
import json
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('filename',action='store', help="Complete path of json file")
args=parser.parse_args()
filename=args.filename

jsondata = json.load(open(filename))
pass_sha = jsondata['passed_job']['trigger_sha']
fail_sha = jsondata['failed_job']['trigger_sha']
repo = jsondata['repo']
gitrepolink = "https://www.github.com/"+str(repo)
gitcomparelink = gitrepolink + "/compare/"+fail_sha+"..."+pass_sha

print("Github link: ",gitrepolink)
print("Github failed trigger commit: ",gitrepolink+"/commit/"+fail_sha)
print("Github passed trigger commit: ",gitrepolink+"/commit/"+pass_sha)
print("Github compare link: ",gitcomparelink)
