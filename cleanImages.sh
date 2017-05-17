#!/bin/bash

for i in ` docker images | grep -v -e IMAGE -e centos -e km3net/km3base | cut -c 41-52 ` ; do echo $i $i && docker rmi $i; done
