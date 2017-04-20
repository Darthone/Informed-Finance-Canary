#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null
daemonize -p /tmp/gather.pid -c ./ -l /tmp/gather.lock -v -e ./error.out -o ./std.out "$SCRIPTPATH/run_rss_watcher.sh"
