FROM km3net/km3base:20160909
MAINTAINER Stefan Geisselsoeder <stefan.geisselsoeder@fau.de>

# you can install DEFINED versions of required software here ...
# BUT DO NOT USE yum update, yum upgrade, yum install, pip install ... for non-fixed software version 
# (please contact the maintainer of the base image for an updated version instead)

RUN yum install -y gnuplot-4.6.2 boost-devel-1.53.0 && yum -y clean all

RUN git clone https://github.com/sgeisselsoeder/multiscale.git /multiscale
RUN make -C /multiscale

COPY externalInput /input

COPY runMultiscaleAnalysis.sh /runMultiscaleAnalysis.sh
RUN chmod 755 runMultiscaleAnalysis.sh

ENTRYPOINT ["/runMultiscaleAnalysis.sh"]

