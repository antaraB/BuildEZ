import re
import os
import xml.etree.ElementTree as xml

#[ERROR] Failed to execute goal org.bsc.maven:maven-processor-plugin:2.2.4:process (process) on project artemis-odb-test: 
#Execution process of goal org.bsc.maven:maven-processor-plugin:2.2.4:process failed: 
#Plugin org.bsc.maven:maven-processor-plugin:2.2.4 or one of its dependencies could not be resolved: 
#Could not find artifact net.onedaybeard.artemis:artemis-odb-processor:jar:2.0.0-RC3-SNAPSHOT -> [Help 1]
#.+ Plugin ([\w\.\:\-]+) or one of its dependencies could not be resolved.+ (Could not find artifact ([\w\.\:\-]+))


input = "[ERROR] Failed to execute goal org.bsc.maven:maven-processor-plugin:2.2.4:process (process) on project artemis-odb-test: Execution process of goal org.bsc.maven:maven-processor-plugin:2.2.4:process failed: Plugin org.bsc.maven:maven-processor-plugin:2.2.4 or one of its dependencies could not be resolved: Could not find artifact net.onedaybeard.artemis:artemis-odb-processor:jar:2.0.0-RC3-SNAPSHOT -> [Help 1]"

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
	print "Inside main function"
	if "Could not find artifact" in input_error : #Convert this to a regex match later.
		print "We are inside the if statement"

		regex_whole_damn_thing = r".+ Plugin ([\w\.\:\-]+) or one of its dependencies could not be resolved.+ (Could not find artifact ([\w\.\:\-]+))"
		grouped_output = re.search(regex_whole_damn_thing, input_error)

		artifact = grouped_output.group(1).split(":")
		print artifact

		#Find the file which needs to be opned.
		#poms = find_all_pom_files("pom.xml","/home/prerit/Spring2018/ECS260/Project/BuildEZ/Code/junkdog")
		poms = find_all_pom_files("pom.xml","/home/travis/build/failed")
		print poms

		#Remove the dependency
		for filepath in poms:
			pomFile = xml.parse(filepath)
			root = pomFile.getroot()

			deps = root.findall(".//xmlns:plugin", namespaces=namespaces)
			for d in deps:
				artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
				version = d.find("xmlns:version", namespaces=namespaces)
				if(artifactId.text == artifact[1]):
					print artifactId.text
					print "Gonna Remove"
					root.find(".//xmlns:plugins", namespaces=namespaces).remove(d)
					print "Removed!"
					pomFile.write(filepath)
					print "File Updated"


if __name__ == '__main__':
	main(input_error)
