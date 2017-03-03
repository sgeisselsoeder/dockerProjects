#!/bin/bash
cd /myAnalysis

echo "Executing analysis"
echo "All output will be stored in /myAnalysis/output/. Do not forget to run this container with \"-v /path/to/folder/you/want/output:/myAnalysis/output/\" if you haven't done so already."
./bin/myAnalysisBinary

echo "Collecting all results to /myAnalysis/output/"
mv outputfile.txt /myAnalysis/output/
chmod -R 777 /myAnalysis/output/

echo "All done!"
