#!/bin/bash
DATETAG=`date +%Y%m%d`
mkdir logs
LOGFILE=logs/build${DATETAG}`date +%H%M%S`.log
IMAGENAME=km3base
echo "creating base image ${IMAGENAME}:${DATETAG}"
docker build -t ${IMAGENAME}:${DATETAG} . 2>&1 | tee ${LOGFILE} 
# REMINDER: Don't use the tag latest here as derived images might change unnoticed if they use :latest
