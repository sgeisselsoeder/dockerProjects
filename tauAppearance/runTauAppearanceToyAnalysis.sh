#!/bin/bash
source /usr/local/bin/thisroot.sh
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/root/

echo "Using inputs from /input"
ln -s /input /tauAppearanceToyAnalysis/input

echo "All output will be stored in /output/. Do not forget to run this container with \"-v /path/to/folder/you/want/output:/output/\" if you haven't done so already."

cd /tauAppearanceToyAnalysis
echo "#########################################"
echo "### Executing tau appearance analysis ###"
echo "#########################################"
echo "smearing the MC truth event tables..."
for file in /input/*.root
do
	echo "INPUT FILE: $file"
	python detectorResolutionSmearing_LoITables.py -f $file -d smearingTables -o histogramsTauappearanceSmeared.root
	break
done

echo "plotting event distribution, bin-wise significance..."
python plotEventDistribution_binSignificance.py -f histogramsTauappearanceSmeared.root

echo "evaluating KM3NeT/ORCA sensitivity to tau-neutrino flux normalisation vs. livetime using toy-MC measurements..."
python simpleEvaluate_tauFluxDetectionSignificance.py -f histogramsTauappearanceSmeared.root

echo "Collecting all results to /output/"
mv *.pdf /output/
mv *.root /output/
chmod -R 777 /output/

echo "All done!"
