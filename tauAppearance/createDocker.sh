#!/bin/bash
DATETAG=`date +%Y%m%d`
ANALYSISBASENAME=tau_appearance_toy
docker build -t ${ANALYSISBASENAME}:${DATETAG} .
