#!/bin/bash
# download the image file and create a container
IMAGETAG=$1
C_NAME=$2
LOCALPATH=../images
docker run -itd --entrypoint=/bin/bash --name="$C_NAME" bugswarm/images:$IMAGETAG
# copy script to container
docker cp $LOCALPATH/diffandgrep.sh $C_NAME:/home/travis/build/diffandgrep.sh
# execute script
docker exec -it $C_NAME /home/travis/build/diffandgrep.sh
# make directory in your local system
mkdir $LOCALPATH/$C_NAME
# copy error files to local directory
docker cp $C_NAME:/home/travis/build/diff.txt $LOCALPATH/$C_NAME/diff.txt
docker cp $C_NAME:/home/travis/build/grep_errors.txt $LOCALPATH/$C_NAME/greperrors.txt
# remove container
docker rm -f $C_NAME
# remove image
docker image rm bugswarm/images:$IMAGETAG
