#!/bin/bash

for i in `docker ps -a | cut -c -12 | grep -v CONTAINER` ; do docker rm $i ; done
