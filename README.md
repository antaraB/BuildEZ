# BuildEZ
Class project that classifies configuration errors encountered on around 100 open source Java projects. We are trying to automate the process of fixing some of these configuration errors.

### Instructions

Run docker/ bugswarm for the image-tag you wish to build

```bash
sudo docker run -itd --entrypoint=/bin/bash --name="$IMAGETAG" bugswarm/images:$IMAGETAG 
docker start -ai $IMAGETAG 
```
OR 
```bash
bugswarm run --image-tag:$IMAGETAG  
```

Once inside the Docker container:

```bash
cd /home/travis/
git clone https://github.com/nehalagrawal/BuildEZ.git
cd BuildEZ
chmod +x scripts/diffandgrep.sh
cd Code
python buildez.py 
```


### Problem Description  

One of the major issues in testing a system is that it fails to build in the test environment. This can be due to a variety of configuration errors: for instance, missing dependencies, malformed build scripts, erroneous configuration variables etc. In this project we propose a study of these configuration errors. We intend to categorize them, and develop an automated solution to resolve them. This will save significant amounts of time for engineers when testing a system, or for users trying to run these projects. 

### Technical Approach 

Firstly, we intend to identify and analyze artifacts indicated as a ‘failed build’ on the BugSwarm platform. We will then categorize the errors into classes. Once these classes are identified we analyse each class to look for possible solutions and apply them to the artifacts. 
Finally we intend to build a system that will automate the process of resolving configuration errors. 

### Evaluation Methodology 

Our evaluation methodology includes : 
- Correctly classifying configuration errors into classes 
- Comparing step by step procedure of resolutions of configuration errors manually vs using an automated system. 
