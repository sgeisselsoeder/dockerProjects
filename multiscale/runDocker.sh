#!/bin/bash

DATETAG=`date +%Y%m%d`
# docker run -v `pwd`/externalOutput:/output multiscale:${DATETAG}
docker run -v `pwd`/externalInput:/input -v `pwd`/externalOutput:/output multiscale:${DATETAG}
