#Original error: Could not transfer metadata com.joyent.http-signature:google-http-client-signature:2.0.0-SNAPSHOT/maven-metadata.xml from/to codehaus-snapshots (https://nexus.codehaus.org/snapshots/): nexus.codehaus.org: unknown error
#-----------------------------------------------------------------------------------------------------------------------------------

#Failed to collect dependencies at com.joyent.http-signature:google-http-client-signature:jar:2.0.0-SNAPSHOT

#-----------------------------------------------------------------------------------------------------------------------------------

#Failed to collect dependencies at com.google.guava:guava:jar:20.0-SNAPSHOT:

#-----------------------------------------------------------------------------------------------------------------------------------

#name - pom.xml and path - /home/travis/build/failed

import re
import os

input_error = None

#STORING PATHS TO ALL POM.XML FILES IN AN ARRAY
def find_all_pom_files(name, path):
	poms = []
	for root, dirs, files in os.walk(path):
		if name in files:
			poms.append(os.path.join(root, name))
	return poms

#OPENING EACH POM FILE TO LOOK FOR THE ONE WITH THE TAG AND REMOVE SNAPSHOT
def find_the_correct_pom_file(patharray):
	tag_description = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[0]
	snapshot = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[1]
	for filepath in patharray:
		newfile = []
		with open(filepath, "w+") as filename:
			for line in filename.readlines():
				if tag_description in line and snapshot in line:
					line = re.sub(r"([\d\.]+)(-SNAPSHOT)",r"\1",line)
				newfile.append(line)
			for line in newfile:
                                filename.write(line)
'''
def find_the_correct_pom_file(patharray):
        #print "Inside find_the_correct_pom_file"
        tag_description = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[0]
        snapshot = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[1]
        #print tag_description, snapshot, patharray
        for filepath in patharray:
                newfile = []
                #print type(filepath)
                with open('%s' % filepath, 'r') as filename:
                        if tag_description in filename.read():
                        #print "------------------------------------------------------------------------"
                        #print filename.readline()
                                for line in filename:
                                        #print line
                                        if tag_description in line and snapshot in line:
                                                line = re.sub(r"([\d\.]+)(-SNAPSHOT)",r"\1",line)
                                                #print "UPDATED LINE"
                                                #print line
                                        newfile.append(line)
                                print newfile
                                filename = open('%s' % filepath, 'w')
                                for line in newfile:
                                        filename.write(line)
                                #print filename.readlines()


'''

#MAIN FUNCTION
def main():
	name = "pom.xml"
	path = "/home/travis/build/failed"
	poms = find_all_pom_files(name, path)
	find_the_correct_pom_file(poms)
if __name__=="__main__":
	main()

