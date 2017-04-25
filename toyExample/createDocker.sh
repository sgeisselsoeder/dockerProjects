#!/bin/bash
DATETAG=`date +%Y%m%d`
ANALYSISBASENAME=my_analysis
docker build -t km3net/${ANALYSISBASENAME}:${DATETAG} .
