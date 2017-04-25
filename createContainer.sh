#!/bin/bash

baseFolder=`pwd`
for folder in km3base toyExample convertRootToHdf5 multiscale tauAppearance
do
	cd $folder
	./createDocker.sh
	cd $baseFolder
done

