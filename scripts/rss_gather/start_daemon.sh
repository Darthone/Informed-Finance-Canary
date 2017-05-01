#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null
WORK=./work/proc/rss
mkdir -p $WORK
daemonize -p $WORK/gather.pid -c ./ -l $WORK/gather.lock -v -e $WORK/error.out -o $WORK/std.out "$SCRIPTPATH/run_rss_watcher.sh"
