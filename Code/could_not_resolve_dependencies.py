import re
import os
import xml.etree.ElementTree as xml
import subprocess

#Failed to execute goal on project projectkorra: 
#Could not resolve dependencies for project com.projectkorra:projectkorra:jar:1.8.2: 
#Could not find artifact org.generallib:GLib:jar:LATEST 
##at specified path /home/travis/build/ProjectKorra/ProjectKorra/lib/GL.jar -> [Help 1]"


#[ERROR] Failed to execute goal on project user-manager: 
#Could not resolve dependencies for project com.peterphi.user-manager:user-manager:war:9.0.2-SNAPSHOT: 
#Could not find artifact AzureLogAppender:AzureLogAppender:jar:1.0 in central (http://repo.maven.apache.org/maven2)


input_error = "Failed to execute goal on project projectkorra: Could not resolve dependencies for project com.projectkorra:projectkorra:jar:1.8.2: Could not find artifact org.generallib:GLib:jar:LATEST at specified path /home/travis/build/ProjectKorra/ProjectKorra/lib/GL.jar -> [Help 1]"



namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}

xml.register_namespace('', 'http://maven.apache.org/POM/4.0.0')
xml.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')


#STORING PATHS TO ALL POM.XML FILES IN AN ARRAY
def find_all_pom_files(name, path):
	poms = []
	for root, dirs, files in os.walk(path):
		if name in files:
			poms.append(os.path.join(root, name))
	return poms

def main(input_error, to_print=False):
	if "Could not find artifact" and "at specified path" in input_error : #Convert this to a regex match later.
		regex_input = r".+ (Could not find artifact ([\w\.\:]+) at specified path ((\/([\w\.+-]+))+)+)"
		grouped_output = re.search(regex_input, input_error)

		artifact = grouped_output.group(2).split(":")

		#Find the file which needs to be opned.
		poms = find_all_pom_files("pom.xml","/home/travis/build/failed")

		for filepath in poms:
			pomFile = xml.parse(filepath)
			root = pomFile.getroot()


			deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
			for d in deps:
				artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
				version = d.find("xmlns:version", namespaces=namespaces)
				systemPath = d.find("xmlns:systemPath", namespaces=namespaces)
				if(artifactId.text == artifact[1]):
					path = systemPath.text
					systemPath.text = systemPath.text.replace(grouped_output.group(5), artifact[1] + "." + artifact[2])
					pomFile.write(filepath)


	else :
		regex_input = r".+ (Could not find artifact ([\w\.\:]+) ([\w\.+-]+))"
		grouped_output = re.search(regex_input, input_error)

		artifact = grouped_output.group(2).split(":")

		#Find the file which needs to be opened.
		poms = find_all_pom_files("pom.xml","/home/travis/build/failed")
		
		#Remove the dependency
		for filepath in poms:
			pomFile = xml.parse(filepath)
			root = pomFile.getroot()
			deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
			for d in deps:
				artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
				version = d.find("xmlns:version", namespaces=namespaces)
				if(artifactId.text == artifact[1]):
					root.find(".//xmlns:dependencies", namespaces=namespaces).remove(d)
					pomFile.write(filepath)

if __name__ == '__main__':
	main(input_error)
