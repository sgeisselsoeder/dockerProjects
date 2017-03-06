FROM km3net/km3base:20160909
MAINTAINER Stefan Geisselsoeder <stefan.geisselsoeder@fau.de>

# you can install DEFINED versions of required software here ...
# BUT DO NOT USE yum update, yum upgrade, yum install, pip install ... for non-fixed software version 
# (please contact the maintainer of the base image for an updated version instead)

# If you really have to install software from the repositories, 
# this is how to check which versions of the software are available in this base image (boost used as example)
# RUN yum list boost
# You MUST then use the specific version to install it, e.g.
# RUN yum -y install boost-1.53.0 && \
#     yum clean all

COPY myAnalysis /myAnalysis 
COPY externalInput /input
COPY runMyAnalysis.sh /runMyAnalysis.sh

RUN make -C /myAnalysis
RUN chmod 755 runMyAnalysis.sh

ENTRYPOINT ["/runMyAnalysis.sh"]

