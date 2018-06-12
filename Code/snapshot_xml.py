#Original error: Could not transfer metadata com.joyent.http-signature:google-http-client-signature:2.0.0-SNAPSHOT/maven-metadata.xml from/to codehaus-snapshots (https://nexus.codehaus.org/snapshots/): nexus.codehaus.org: unknown error
#-----------------------------------------------------------------------------------------------------------------------------------

#Failed to collect dependencies at com.joyent.http-signature:google-http-client-signature:jar:2.0.0-SNAPSHOT

#-----------------------------------------------------------------------------------------------------------------------------------

#Failed to collect dependencies at com.google.guava:guava:jar:20.0-SNAPSHOT:

#-----------------------------------------------------------------------------------------------------------------------------------

#name - pom.xml
#path - /home/travis/build/failed
from __future__ import print_function
import re
import os
import xml.etree.ElementTree as xml
import subprocess

#input_error = "Failed to collect dependencies at com.joyent.http-signature:google-http-client-signature:jar:2.0.0-SNAPSHOT"
#input_error2 = "Failed to collect dependencies at com.google.guava:guava:jar:20.0-SNAPSHOT"

#STORING PATHS TO ALL POM.XML FILES IN AN ARRAY
def find_all_pom_files(name, path, to_print=False):
        if to_print:
                print ("-------------Inside find_all_pom_files-----------------")
        poms = []
        for root, dirs, files in os.walk(path):
                if name in files:
                        poms.append(os.path.join(root, name))
        return poms

#OPENING EACH POM FILE TO LOOK FOR THE ONE WITH THE TAG AND REMOVE SNAPSHOT
def find_the_correct_pom_file(patharray, input_error, to_print = False):
        tag_description = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[0]
        snapshot = re.search(r"\:([\w-]+)\:jar\:([\d\.]+-SNAPSHOT)",input_error).groups()[1]
        if to_print:
                print ("--------------Inside find_the_correct_pom_file------------")
                print ("Tag :",tag_description, " | Snapshot version: ",snapshot, " | Path array: ",patharray)
        for filepath in patharray:
                with open('%s' % filepath, 'r') as filename:
                        if tag_description in filename.read():
                                pomfile = xml.parse(filepath)
                                if to_print:
                                        print ("POM file: ",pomfile)
                                root = pomfile.getroot()
                                namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}
                                xml.register_namespace('', 'http://maven.apache.org/POM/4.0.0')
                                xml.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
                                properties = root.find(".//xmlns:properties", namespaces = namespaces)
                                for p in properties.iter():
                                        if p.text == snapshot:
                                                p.text = re.sub(r"(.+)(-SNAPSHOT)",r"\1", p.text)
                                                if to_print:
                                                        print ("Line changed: ",p.text)
                                                pomfile.write(filepath)

#MAIN FUNCTION
def main(input_error, to_print=False):
        if to_print:
                print ("---------INSIDE MAIN (snapshot_xml)------------")
        name = "pom.xml"
        path = "/home/travis/build/failed"
        poms = find_all_pom_files(name, path, to_print)
        if to_print:
                print ("-------ARRAY RETURNED BY THE FUNCTION---\n",poms)
        find_the_correct_pom_file(poms, input_error, to_print)

if __name__=="__main__":
        main(input_error)

