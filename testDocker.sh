#!/bin/bash

DATETAG=`date +%Y%m%d`
baseFolder=`pwd`
for folder in toyExample convertRootToHdf5 multiscale tauAppearance
do
	cd $folder
	./runDocker.sh
	cd $baseFolder
done

