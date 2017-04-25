#!/bin/bash

DATETAG=`date +%Y%m%d`
#docker run -v `pwd`/hostOutput:/output km3net/multiscale:${DATETAG}
docker run -v `pwd`/hostInput:/input -v `pwd`/hostOutput:/output km3net/multiscale:${DATETAG}
#docker run -v `pwd`/hostInput:/input -v `pwd`/hostOutput:/output km3net/multiscale:20170318
