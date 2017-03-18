FROM km3net/km3base:20170318

MAINTAINER Steffen Hallmann <steffen.hallmann@fau.de>

#############################################
### toy analysis for tau-appearance study ###
#############################################

### copy files for analysis
ENV ANALYSISDIR /tauAppearanceToyAnalysis
COPY tauAppearanceToyAnalysis $ANALYSISDIR
COPY externalInput /input
COPY runTauAppearanceToyAnalysis.sh /runTauAppearanceToyAnalysis.sh
RUN chmod 755 /runTauAppearanceToyAnalysis.sh

ENTRYPOINT ["/runTauAppearanceToyAnalysis.sh"]

