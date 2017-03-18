FROM centos:latest

MAINTAINER Stefan Geißelsöder <stefan.geisselsoeder@fau.de>

# everything is in one command to avoid itnermediate layers (saves space)
#RUN yum -y install centos-release-scl && \
RUN mkdir -p /input && mkdir -p /output && \
    yum -y update && \
    yum -y upgrade && \
    yum -y install --setopt=tsflags=nodocs \
    automake \
    autoconf \
    bash \
    cvs \
    gcc \
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
    make gcc gcc-c++ gcc-gfortran \
    cmake zlib-devel\
    openmpi openmpi-devel \
    fftw fftw-devel \
    gsl gsl-devel gmp \
    python-devel \
    docutils python-nose \
    python-docutils \
    hdf5 hdf5-devel \
    lzo-devel \ 
    lbzip2 bzip2-devel blosc blosc-devel \
    && yum -y remove python-setuptools && \ 
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && \ 
    python get-pip.py && rm get-pip.py && \
    pip install cython numpy h5py setuptools && \
    pip install km3pipe && \
    yum -y clean all 
#    devtoolset-4-gcc* \

RUN mkdir /tmp/root -p && cd /tmp/root/ && \
    wget https://root.cern.ch/download/root_v5.34.36.source.tar.gz && \
    tar xf root_v5.34.36.source.tar.gz && \ 
    cd root && \
    ./configure linuxx8664gcc --enable-python --prefix=/usr/local && \
    make -j 2 ; make -j 2 ; make -j 2 ; make -j 2 && \
    make install && \
    cd / && \
    rm -rf /tmp/root \
    && source /usr/local/bin/thisroot.sh && env
ENV ROOTSYS /usr/local
ENV LD_LIBRARY_PATH /usr/local/lib/root
ENV LIBPATH /usr/local/lib/root
ENV DYLD_LIBRARY_PATH /usr/local/lib/root
ENV PYTHONPATH /usr/local/lib/root
ENV SHLIB_PATH /usr/local/lib/root

#RUN wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-8.noarch.rpm && rpm -ivh epel-release-7-8.noarch.rpm

#RUN yum -y install --setopt=tsflags=nodocs bison bison-devel ant flex flex-devel ghostscript compat-gcc-34-g77 \
#    && yum -y clean all 
#RUN yum -y install --setopt=tsflags=nodocs \
#    libX11 libX11-devel libXpm libXpm-devel libXft libXft-devel libX11-common libXext libXext-devel \
#    && yum -y clean all 
#RUN yum -y install --setopt=tsflags=nodocs \
#    openjdk-7-jdk \
#    zsh \
#    fftw-devel \
#    && yum -y clean all 


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

ENTRYPOINT ["/bin/bash"]
