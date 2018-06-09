#[ERROR] Failed to execute goal org.bsc.maven:maven-processor-plugin:2.2.4:process (process) on project artemis-odb-test: 
#Execution process of goal org.bsc.maven:maven-processor-plugin:2.2.4:process failed: 
#Plugin org.bsc.maven:maven-processor-plugin:2.2.4 or one of its dependencies could not be resolved: 
#Could not find artifact net.onedaybeard.artemis:artemis-odb-processor:jar:2.0.0-RC3-SNAPSHOT -> [Help 1]
#.+ Plugin ([\w\.\:\-]+) or one of its dependencies could not be resolved.+ (Could not find artifact ([\w\.\:\-]+))


input = "[ERROR] Failed to execute goal org.bsc.maven:maven-processor-plugin:2.2.4:process (process) on project artemis-odb-test: Execution process of goal org.bsc.maven:maven-processor-plugin:2.2.4:process failed: Plugin org.bsc.maven:maven-processor-plugin:2.2.4 or one of its dependencies could not be resolved: Could not find artifact net.onedaybeard.artemis:artemis-odb-processor:jar:2.0.0-RC3-SNAPSHOT -> [Help 1]"

namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}


#STORING PATHS TO ALL POM.XML FILES IN AN ARRAY
def find_all_pom_files(name, path):
	poms = []
	for root, dirs, files in os.walk(path):
		if name in files:
			poms.append(os.path.join(root, name))
	return poms

def main():
	print "Inside main function"
	if "Could not find artifact" in input : #Convert this to a regex match later.
		print "We are inside the if statement"

		regex_whole_damn_thing = r".+ Plugin ([\w\.\:\-]+) or one of its dependencies could not be resolved.+ (Could not find artifact ([\w\.\:\-]+))"
		grouped_output = re.search(regex_whole_damn_thing, input)

		artifact = grouped_output.group(1).split(":")
		print artifact

		#Find the file which needs to be opned.
		poms = find_all_pom_files("pom.xml","/home/prerit/Spring2018/ECS260/Project/BuildEZ/Code/junkdog")
		#poms = find_all_pom_files("pom.xml","/home/travis/build/failed")
		print poms

		# for filepath in poms:
		# 	pomFile = xml.parse(filepath)
		# 	root = pomFile.getroot()


		# 	deps = root.findall(".//xmlns:dependency", namespaces=namespaces)
		# 	for d in deps:
		# 		artifactId = d.find("xmlns:artifactId", namespaces=namespaces)
		# 		version = d.find("xmlns:version", namespaces=namespaces)
		# 		systemPath = d.find("xmlns:systemPath", namespaces=namespaces)
		# 		if(artifactId.text == artifact[1]):
		# 			print systemPath.text
		# 			path = systemPath.text
		# 			systemPath.text = systemPath.text.replace(grouped_output.group(5), artifact[1] + "." + artifact[2])
		# 			print systemPath.text
		# 			pomFile.write(filepath)


if __name__ == '__main__':
	main()
