#!/bin/bash

echo "git pull is not applied because of naswork samba directory build"
echo " build automatically without git check"
exit 0

LC_ALL=C git reset --hard origin/master
LC_ALL=C git pull | tee dirty.txt 

grep "error" dirty.txt
if [ $? -eq 0 ];then
	cat dirty.txt
	echo "Error on git pull"
	exit 9
fi

grep "Already up to date" dirty.txt
if [ $? -eq 0 ];then
	echo "Noting changed!"
	rm -f dirty.txt
	exit 0
else
	echo "Something changed!"
	cat dirty.txt
	exit 0
fi
