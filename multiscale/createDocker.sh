#!/bin/bash
DATETAG=`date +%Y%m%d`
ANALYSISBASENAME=multiscale
docker build -t km3net/${ANALYSISBASENAME}:${DATETAG} .
