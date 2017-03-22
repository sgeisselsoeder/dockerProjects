#!/bin/bash

for f in /input/*.root
do
	tohdf5 $f
done

mv /input/*.h5 /output
chmod -R 777 /output
