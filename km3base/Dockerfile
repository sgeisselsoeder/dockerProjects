FROM centos:latest

MAINTAINER Stefan Geißelsöder <stefan.geisselsoeder@fau.de>

RUN yum -y update && \
    yum -y upgrade && \
    yum -y clean all

RUN yum -y install --setopt=tsflags=nodocs \
    automake \
    autoconf \
    cvs \
    gcc \
    gcc-c++ \
    git \
    make \
    subversion \
    boost \
    libstdc++ \ 
    bison \
    zip \
    unzip \
    wget \
    && yum -y clean all 

# TODO: this is an intermediate state. must be cleaned before a new base image is released

RUN wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-8.noarch.rpm && rpm -ivh epel-release-7-8.noarch.rpm

RUN yum -y update && \
    yum -y upgrade && \
    yum -y clean all

RUN yum -y install --setopt=tsflags=nodocs bison bison-devel ant flex flex-devel ghostscript compat-gcc-34-g77 \
    && yum -y clean all 
RUN yum -y install --setopt=tsflags=nodocs \
    libX11 libX11-devel libXpm libXpm-devel libXft libXft-devel libX11-common libXext libXext-devel \
    && yum -y clean all 
RUN yum -y install --setopt=tsflags=nodocs \
    openjdk-7-jdk \
    zsh \
    fftw-devel \
    && yum -y clean all 

RUN yum -y install --setopt=tsflags=nodocs \
    bzip2 \
    binutils \
    python \
    redhat-lsb-core \
    gcc-gfortran \ 
    openssl-devel \ 
    pcre-devel \ 
    python-numpy-devel \
    gsl-static \
    libX11-devel libXpm-devel libXft-devel libXext-devel \
    && yum -y clean all 


RUN mkdir /tmp/root -p && cd /tmp/root/ && \
    wget https://root.cern.ch/download/root_v5.34.36.source.tar.gz && \
    tar xf root_v5.34.36.source.tar.gz && \ 
    pwd && ls && \
    cd root && \
    ./configure linuxx8664gcc --enable-python --prefix=/usr/local && \
    make && \
    make install && \
    rm -rf /tmp/root

#TODO ENV root pfade setzen

RUN yum install -y make gcc gcc-c++ gcc-gfortran \
    cmake zlib-devel\
    openmpi openmpi-devel \
    fftw fftw-devel \
    gsl gsl-devel gmp \
    python-devel \
    docutils python-nose \
    python-docutils
    # numpy numpy-f2py\

RUN yum install -y hdf5 hdf5-devel	# tell tom about these requirements

RUN yum install -y lzo-devel	# tell tom about these requirements
RUN yum install -y lbzip2 bzip2-devel blosc blosc-devel	# tell tom about these requirements

# RUN yum install -y numpy numpy-f2py
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && python get-pip.py && pip install cython numpy h5py
RUN pip install km3pipe



# jpp stuff
# RUN svn checkout --non-interactive --no-auth-cache --username km3net --password the-default-km3net-pw http://svn.km3net.de/Jpp/trunk /Jpp && \
#    cd /Jpp && \
#    ls && \
#    cat Makefile 
# RUN SHELL="/bin/bash" && \
#    cd /Jpp && \
#    source /usr/local/bin/thisroot.sh && \ 
#    source setenv.sh && \
#    make

# TODO: maybe defunc yum update, yum upgrade, yum install etc ... (= defunc yum); alias doesn't work

ENTRYPOINT ["/bin/bash"]
