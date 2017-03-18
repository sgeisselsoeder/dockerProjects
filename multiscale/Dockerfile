FROM km3net/km3base:20170318
MAINTAINER Stefan Geisselsoeder <stefan.geisselsoeder@fau.de>

# you can install DEFINED versions of required software here ...
# BUT DO NOT USE yum update, yum upgrade or yum install, pip install, etc. for non-fixed software version 
# (please contact the maintainer of the base image for an updated version instead)

RUN yum install -y gnuplot-4.6.2 boost-devel-1.53.0 && yum -y clean all

RUN git clone https://github.com/sgeisselsoeder/multiscale.git /multiscale
RUN make -C /multiscale

# For this analysis demo we will either mount the input or have a default setup be created on the fly
# COPY externalInput /input

COPY runMultiscaleAnalysis.sh /runMultiscaleAnalysis.sh
RUN chmod 755 runMultiscaleAnalysis.sh

ENTRYPOINT ["/runMultiscaleAnalysis.sh"]

