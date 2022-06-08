FULL_BUILD=0
if [ $# -eq 0 ]; then
	echo "partially build mode"
    echo ${FULL_BUILD}
else
    if [ "$1" = "-f" ]; then
        echo "fully build mode"
        FULL_BUILD=1
        echo ${FULL_BUILD}
    else
        echo "unrecognized inp, use -f to run fully build mode, now remain in partially build mode"
    fi
fi

export FULL_BUILD_C=1

rm -r build
mkdir build
if [ $FULL_BUILD -eq 1 ]; then
    cd build
    rm -r ./*
    cmake ..
    make -j7
fi