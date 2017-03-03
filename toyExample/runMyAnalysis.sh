#!/bin/bash
cd /myAnalysis

echo "Executing analysis"
./bin/myAnalysisBinary

echo "Collecting all results to /myAnalysis/output/"
mv outputfile.txt /myAnalysis/output/
chmod -R 777 /myAnalysis/output/

echo "All done!"
