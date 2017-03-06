#!/bin/bash

echo "Using inputs from /input"
ln -s /input /myAnalysis/input

echo "All output will be stored in /output/. Do not forget to run this container with \"-v /path/to/folder/you/want/output:/output/\" if you haven't done so already."

cd /myAnalysis
echo "Executing analysis"
./bin/myAnalysisBinary

echo "Collecting all results to /output/"
mv outputfile.txt /output/
chmod -R 777 /output/

echo "All done!"
