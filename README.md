# BuildEZ
(Project for SQ18 ECS 260)

#### Abstract
Building is an essential step in the software development process. However, programmers frequently face build failures that reduce productivity and slow down the development process. Analyzing these errors can help build tools to automate the process of resolving them. In this project, we analyze and categorize build failures of 100 open source Java projects by examining artifacts from the BugSwarm dataset. We select the most common category (dependency errors) and build scripts to automate the process of resolving the failures.  We also evaluate these fixes on a set of new image-tags.


### Instructions

To fix a given build, replace $IMAGETAG with the image-tag you wish to fix. You can find a list of image-tags for [builds that get fixed here](image_tag_files/passing-tags) and [all dependency errors in general here](image_tag_files/dependency-tags)

Select one tag and follow the given instructions:

#### Step 1: Run docker/ bugswarm for the image-tag you wish to build

```bash
sudo docker run -itd --entrypoint=/bin/bash --name="$IMAGETAG" bugswarm/images:$IMAGETAG 
docker start -ai $IMAGETAG 
```
OR 
```bash
bugswarm run --image-tag:$IMAGETAG  
```

#### Step 2:  Inside the Docker container:

```bash
cd /home/travis/
git clone https://github.com/nehalagrawal/BuildEZ.git
cd BuildEZ
# make diffandgrep.sh executable. This script greps all "ERROR" messages from the failed build-log and stores it in /home/travis/grep_errors.txt
chmod +x scripts/diffandgrep.sh
cd code
# buildez.py is the driver function. It reads from grep_errors.txt and attempts to fix the build.
python buildez.py 
```
To print intermediate messages on buildez.py, run it with -v or --verbose option. To print the build messages, run it with -b or --build-output option
Eg:
```bash
python buildez.py -vb 
# will print both intermediate messages and build output
# See python buildez.py -h for more information  
```

The script will print if the build ultimates passes or fails.