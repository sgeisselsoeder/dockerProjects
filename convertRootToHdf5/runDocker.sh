#!/bin/bash
DATETAG=`date +%Y%m%d`
ANALYSISBASENAME=km3net/convert_root_to_hdf5

docker run -v `pwd`/hostInput:/input -v `pwd`/hostOutput:/output ${ANALYSISBASENAME}:${DATETAG}
