#!/bin/bash

# $Id: i3-install.sh 45510 2008-05-19 01:30:34Z blaufuss $

# 
# Default package to install
#
PACKAGE=i3-tools-km3net-v4
export CPPFLAGS=-I/usr/kerberos/include
export LDFLAGS=-L/usr/X11/lib

CURL=`which curl`

if [ -z "$CURL" ]
then
    echo "Program 'curl' not found.   Please install and put in path."
    exit 2
else
    echo "Curl found at $CURL"
fi

if [ -z $1 ]
then
    echo "Usage: i3-install.sh installation_prefix"
    echo "Please supply an installation prefix"
    exit 2
fi

if [ -a $1 ]
then
    echo "===> Specified prefix $1 exists."
    echo "===> Please remove it before proceeding"
    exit 2
fi

if [ -f /usr/lib/tclConfig.sh ]
then
    TCL_CONFIG=/usr/lib
elif [ -f /usr/lib64/tclConfig.sh ]
then
    TCL_CONFIG=/usr/lib64
elif [ -f /usr/lib/tcl8.4/tclConfig.sh ]
then
    TCL_CONFIG=/usr/lib/tcl8.4
else
    echo "===> No Tcl configuration was found on this system.  Please ensure"
    echo "===> your Tcl installation is complete before proceeding."
    exit 2
fi

if [ -f ./Makefile ] ; then
    make clean
fi

./configure --prefix=$1  --with-tcl=${TCL_CONFIG}
make
make install
cd $1
./bin/port sync

rm -f var/db/dports/sources/rsync.code.km3net.physik.uni-erlangen.de_icetray-tools-ports/science/igraph_0.5.4/Portfile
cp /hotfixes/igraphPortfile var/db/dports/sources/rsync.code.km3net.physik.uni-erlangen.de_icetray-tools-ports/science/igraph_0.5.4/Portfile

./bin/port install $PACKAGE
