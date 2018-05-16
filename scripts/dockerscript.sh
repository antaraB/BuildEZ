#!/bin/bash
# download the image file and create a container
IMAGETAG=$1
C_NAME=$2
LOCALPATH=../images
sudo docker run -itd --entrypoint=/bin/bash --name="$C_NAME" bugswarm/images:$IMAGETAG
# copy script to container
sudo docker cp $LOCALPATH/diffandgrep.sh $C_NAME:/home/travis/build/diffandgrep.sh
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