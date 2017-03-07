#!/bin/bash

externalInput="/input/events.txt"
echo "If you haven't overwritten the file" ${externalInput}", the default will be used:"
echo "A random distribution of 13283 events"
echo "+ artificial source, 49 events, declination -52.5, right ascension 260, radius 3"
echo "+ artificial source, 18 events, declination +4, right ascension 160, radius 1"
echo "+ artificial source, 74 events, declination -22.5, right ascension 55, radius 5"

cd /multiscale/

if [ -e $externalInput ]; 
then 
	echo "Using inputs from " ${externalInput}
	cp $externalInput /multiscale/input/events.txt
	echo "Executing evaluation without significance computation (the required pseudo experiments would take very long on a single machine)"
	echo "Reminder: All output will be stored in /output/. Please don't forget to run this container with \"-v /path/to/folder/you/want/output:/output/\" (if you haven't done so already)."
	./pipelines/pipelineLocalInputEvaluation.sh

else
	echo "Using default inputs"
	echo "If you want to use your own data, please supply a file mounted to " ${externalInput}
	echo "Executing evaluation without significance computation (the required pseudo experiments would take very long on a single machine)"
	echo "Reminder: All output will be stored in /output/. Please don't forget to run this container with \"-v /path/to/folder/you/want/output:/output/\" (if you haven't done so already)."
	./pipelines/pipelineLocalArtificialSources.sh

fi

echo "Collecting all results to /output/"
mv ./output/scenarioEvaluation/hammerProjEquatorial.txt /output/
mv ./output/scenarioEvaluation/skymapEquatorialWithEvents.pdf /output/
mv ./output/scenarioEvaluation/eventsEquatorial.pdf /output/
mv ./output/scenarioEvaluation/equatorialFineCoarse.pdf /output/skymapEquatorial.pdf
chmod -R 777 /output/

echo "All done! Thank you for your patience."
