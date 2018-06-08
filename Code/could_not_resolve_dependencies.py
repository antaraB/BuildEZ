import re
import os

#Failed to execute goal on project projectkorra: 
#Could not resolve dependencies for project com.projectkorra:projectkorra:jar:1.8.2: 
#Could not find artifact org.generallib:GLib:jar:LATEST 
#at specified path /home/travis/build/ProjectKorra/ProjectKorra/lib/GL.jar -> [Help 1]"


input = "Failed to execute goal on project projectkorra: Could not resolve dependencies for project com.projectkorra:projectkorra:jar:1.8.2: Could not find artifact org.generallib:GLib:jar:LATEST at specified path /home/travis/build/ProjectKorra/ProjectKorra/lib/GL.jar -> [Help 1]"
input2 = "[ERROR] Failed to execute goal on project user-manager: Could not resolve dependencies for project com.peterphi.user-manager:user-manager:war:9.0.2-SNAPSHOT: Could not find artifact AzureLogAppender:AzureLogAppender:jar:1.0 in central (http://repo.maven.apache.org/maven2)"


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
		with open(filepath, w+) as filename:
			for line in filename:
				if tag_description in line and snapshot in line:
					line = re.sub(r"([\d\.]+)(-SNAPSHOT)",r"\1",line)
				newfile.append(line)
			filename.write(newfile)


def main():
	print "Inside main function"
	if "Could not find artifact" and "at specified path" in input : #Convert this to a regex match later.
		print "We are inside the if statement"
		# inputarray = input.split(": ")
		# print inputarray
		# regex_path = r"((\/([\w\.+-]+))+)+"
		regex_whole_damn_thing = r".+ (Could not find artifact ([\w\.\:]+) at specified path ((\/([\w\.+-]+))+)+)"
		grouped_output = re.search(regex_whole_damn_thing, input)
		print grouped_output.groups()
		print grouped_output.group(1)
		print grouped_output.group(2)
		print grouped_output.group(3)
		print grouped_output.group(4)
		print grouped_output.group(5)

		#Find the file which needs to be opned.
		poms = find_all_pom_files("pom.xml","/home/travis/build/failed")
		print "POMSSSS"
		print poms

		#Replace the error of the file
		find_the_correct_pom_file(poms)

		#Check if the fix works.
	else :
		print "We are inside else statement"
		regex_whole_damn_thing = r".+ (Could not find artifact ([\w\.\:]+) ([\w\.+-]+))"
		grouped_output = re.search(regex_whole_damn_thing, input)
		print grouped_output.groups()
		print grouped_output.group(1)
		print grouped_output.group(2)
		print grouped_output.group(3)
		#Find the pom.xml file. 
		#Remove the dependency
		#Check if it is working

if __name__ == '__main__':
	main()
