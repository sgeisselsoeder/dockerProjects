#!/bin/bash
DATETAG=`date +%Y%m%d`
ANALYSISBASENAME=km3net/convert_root_to_hdf5
docker build -t ${ANALYSISBASENAME}:${DATETAG} .
