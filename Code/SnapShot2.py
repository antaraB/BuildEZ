#Original error: Could not transfer metadata com.joyent.http-signature:google-http-client-signature:2.0.0-SNAPSHOT/maven-metadata.xml from/to codehaus-snapshots (https://nexus.codehaus.org/snapshots/): nexus.codehaus.org: unknown error
#-----------------------------------------------------------------------------------------------------------------------------------

#Failed to collect dependencies at com.joyent.http-signature:google-http-client-signature:jar:2.0.0-SNAPSHOT

#-----------------------------------------------------------------------------------------------------------------------------------

#Failed to collect dependencies at com.google.guava:guava:jar:20.0-SNAPSHOT:

#-----------------------------------------------------------------------------------------------------------------------------------

#name - pom.xml
#path - /home/travis/build/failed


import re
import os
import xml.etree.ElementTree as xml
import subprocess

input_error = "Failed to collect dependencies at com.joyent.http-signature:google-http-client-signature:jar:2.0.0-SNAPSHOT"
input_error2 = "Failed to collect dependencies at com.google.guava:guava:jar:20.0-SNAPSHOT"

#STORING PATHS TO ALL POM.XML FILES IN AN ARRAY
def find_all_pom_files(name, path):
        print "-------------Inside find_all_pom_files-----------------"
        poms = []
        for root, dirs, files in os.walk(path):
                if name in files:
                        poms.append(os.path.join(root, name))
        return poms

#OPENING EACH POM FILE TO LOOK FOR THE ONE WITH THE TAG AND REMOVE SNAPSHOT
def find_the_correct_pom_file(patharray):
        print "--------------Inside find_the_correct_pom_file------------"
        tag_description = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[0]
        snapshot = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[1]
        print tag_description, snapshot, patharray
        for filepath in patharray:
                with open('%s' % filepath, 'r') as filename:
                        if tag_description in filename.read():
                                pomfile = xml.parse(filepath)
                                print pomfile
                                root = pomfile.getroot()
                                namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
                                properties = root.find(".//xmlns:properties", namespaces = namespaces)
                                snap = properties.find(".//xmlns:dependency." + tag_description + ".version", namespaces = namespaces)
                                #print snap.text
                                snap.text = re.sub(r"(.+)(-SNAPSHOT)",r"\1",snap.text)
                                print snap.text
                                pomfile.write(filepath)
                                print pomfile
'''
#REBUILDING PROJECT AFTER FIXING POM FILE
def rebuild_using_new_pom():
	result = subprocess.call('/usr/local/bin/run_failed.sh')
	#print result
	if result == 0:
		print "Build passed!! WOOOHOOOOO!"
	elif result == 2:
		print "MAA KI AANKH!"
'''
#MAIN FUNCTION
def main():
        print "---------INSIDE MAIN------------"
        name = "pom.xml"
        path = "/home/travis/build/failed"
        poms = find_all_pom_files(name, path)
        print "-------ARRAY RETURNED BY THE FUNCTION---"
        print poms
        find_the_correct_pom_file(poms)
        #rebuild_using_new_pom()
if __name__=="__main__":
	main()

