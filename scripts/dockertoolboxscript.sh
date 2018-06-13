#!/bin/bash
# download the image file and create a container
# first argument should be file containing all the images
LOCALPATH=../images/latest
IMAGES=()
# copy all image-tags from file to an array
mapfile -t IMAGES < $1

for i in ${IMAGES[@]};
do
	IMAGETAG=$i
	C_NAME=$i
	docker run -itd --entrypoint=/bin/bash --name="$C_NAME" bugswarm/images:$IMAGETAG
	echo "Running container for image $IMAGETAG"
	# copy script to container
	docker cp ./diffandgrep.sh $C_NAME:/home/travis/build/diffandgrep.sh
	# execute script
	docker exec -it $C_NAME /home/travis/build/diffandgrep.sh
	# make directory in your local system (if it doesn't already exist)
	mkdir -p $LOCALPATH/$C_NAME
	# copy error files to local directory
	docker cp $C_NAME:/home/travis/build/diff.txt $LOCALPATH/$C_NAME/diff.txt
	docker cp $C_NAME:/home/travis/build/grep_errors.txt $LOCALPATH/$C_NAME/greperrors.txt
	# remove container
	docker rm -f $C_NAME
	# remove image
	docker image rm bugswarm/images:$IMAGETAG
	echo "Finished processing for image $IMAGETAG"
done


