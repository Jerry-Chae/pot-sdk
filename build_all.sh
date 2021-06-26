#!/bin/bash

# next is for Mac brew
export PATH=$PATH:/usr/local/bin

# do not check dirty (instead use network mount)
## 1) check if dirty.txt exists or not
#if [ ! -e dirty.txt ];then
#	echo "Nothing to build!"
#	exit 0
#fi

# 2) pkg
pip3 install PyYAML

# 3) 쉘 스크립트가 있는 디레터리 위치 구함
WDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
echo "working directory for build_all is \"${WDIR}\""

# 4) alabs.ppm 부터 작업
BDIR=${WDIR}/alabs/ppm
bf=${BDIR}/build.sh
python3 ${WDIR}/change_version.py -n ${BDIR}/setup.yaml
pushd ${BDIR}
    bash build.sh
    if [ $? -ne 0 ];then
        echo "Error!!!"
        exit 9
    fi
popd
echo "building ${bf} done!"

# 5) alabs.common 작업 (공통 라이브러리)
BDIR=${WDIR}/alabs/common
bf=${BDIR}/build.sh
python3 ${WDIR}/change_version.py -n ${BDIR}/setup.yaml
pushd ${BDIR}
    bash build.sh
    if [ $? -ne 0 ];then
        echo "Error!!!"
        exit 9
    fi
popd
echo "building ${bf} done!"

# 5) 해당 디렉터리에서 재귀적으로 build.sh 를 구하여 $bf로 작업
for bf in $(find ${WDIR} -name "build.sh");do
    echo "building ${bf} ..."
    BDIR=$(dirname ${bf})
    if [ "${BDIR}" == "${WDIR}/alabs/ppm" ];then
        continue
    fi
    if [ "${BDIR}" == "${WDIR}/alabs/common" ];then
        continue
    fi
    python3 ${WDIR}/change_version.py -n ${BDIR}/setup.yaml
    pushd ${BDIR}
        bash build.sh
        if [ $? -ne 0 ];then
            echo "Error!!!"
            exit 9
        fi
    popd
    echo "building ${bf} done!"
done
echo "Build All is done!"
exit 0
