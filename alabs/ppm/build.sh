#!/bin/bash

pip3 install PyYAML
PYTHONPATH=../.. python3 test_ppm.py
if [ $? -ne 0 ];then
	echo "ppm test, build, upload ERROR!"
	exit 9
fi
echo "ppm test, build, upload Success!"
exit 0
