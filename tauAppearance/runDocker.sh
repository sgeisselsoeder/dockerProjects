#!/bin/bash
DATETAG=`date +%Y%m%d`
ANALYSISBASENAME=tau_appearance_toy
# run the docker container with a mapping of the local output folder to the output folder in the container
# NOTE: both MUST be absolute paths, relative paths are not allowed
docker run -v `pwd`/hostOutput:/output km3net/${ANALYSISBASENAME}:${DATETAG}
