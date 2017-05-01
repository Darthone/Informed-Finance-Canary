#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null
WORK=./work/proc/loader
mkdir -p $WORK
daemonize -p $WORK/loader.pid -c ./ -l $WORK/loader.lock -v -e $WORK/error.out -o $WORK/std.out "$SCRIPTPATH/run_loader.sh"
