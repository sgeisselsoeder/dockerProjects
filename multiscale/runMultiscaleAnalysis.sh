#!/bin/bash

cd /multiscale/

externalInput="/input/events.txt"
if [ -e $externalInput ]; 
then 
	echo "Using inputs from " ${externalInput}
	cp $externalInput /multiscale/input/events.txt
	echo "Executing evaluation without significance computation (the required pseudo experiments would take very long on a single machine)"
	echo "Reminder: All output will be stored in /output/. Please don't forget to run this container with \"-v /path/to/folder/you/want/output:/output/\" (if you haven't done so already)."
	./pipelines/pipelineLocalInputEvaluation.sh

else
	echo "Using default inputs (random distribution, three artificial sources)"
	echo "If you want to use your own data, please supply a file mounted to " ${externalInput}
	echo "Executing evaluation without significance computation (the required pseudo experiments would take very long on a single machine)"
	echo "Reminder: All output will be stored in /output/. Please don't forget to run this container with \"-v /path/to/folder/you/want/output:/output/\" (if you haven't done so already)."
	./pipelines/pipelineLocalArtificialSources.sh

fi

echo "Collecting all results to /output/"
mv ./output/scenarioEvaluation/hammerProjEquatorial.txt /output/
mv ./output/scenarioEvaluation/*.pdf /output/
chmod -R 777 /output/

echo "All done! Thank you for your patience."
