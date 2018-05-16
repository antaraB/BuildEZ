#!/bin/bash
# download the image file and create a container
# first argument should be file containing all the image-tags
LOCALPATH=../images
IMAGES=()
# copy all image-tags from file to an array
mapfile -t IMAGES < $1

for i in ${IMAGES[@]};
do
	IMAGETAG=$i
	C_NAME=$i
	sudo docker run -itd --entrypoint=/bin/bash --name="$C_NAME" bugswarm/images:$IMAGETAG
	echo "Running container for image $IMAGETAG"
	# copy script to container
	sudo docker cp ./diffandgrep.sh $C_NAME:/home/travis/build/diffandgrep.sh
	# execute script
	sudo docker exec -it $C_NAME /home/travis/build/diffandgrep.sh
	# make directory in your local system
	mkdir $LOCALPATH/$C_NAME
	# copy error files to local directory
	sudo docker cp $C_NAME:/home/travis/build/diff.txt $LOCALPATH/$C_NAME/diff.txt
	sudo docker cp $C_NAME:/home/travis/build/grep_errors.txt $LOCALPATH/$C_NAME/greperrors.txt
	# remove container
	sudo docker rm -f $C_NAME
	# remove image
	sudo docker image rm bugswarm/images:$IMAGETAG
	echo "Finished processing for image $IMAGETAG"
	bugswarm show --image-tag $IMAGETAG > $LOCALPATH/$C_NAME/bugswarm_output
	python read_bugswarm.py $LOCALPATH/$C_NAME/bugswarm_output > $LOCALPATH/$C_NAME/bugswarm_info.txt
done