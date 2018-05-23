#!/bin/bash
# run bugswarm show on all image tags and save important info to relevant file 
# first argument should be file containing all the image-tags
LOCALPATH=../images/latest_nehal
IMAGES=()
# copy all image-tags from file to an array
mapfile -t IMAGES < $1

for i in ${IMAGES[@]};
do
	IMAGETAG=$i
	C_NAME=$i
	mkdir -p $LOCALPATH/$C_NAME
	bugswarm show --image-tag $IMAGETAG > $LOCALPATH/$C_NAME/bugswarm_output
	python read_bugswarm.py $LOCALPATH/$C_NAME/bugswarm_output > $LOCALPATH/$C_NAME/bugswarm_info.txt
	echo "Finished processing $IMAGETAG"
done
