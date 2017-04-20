#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null
daemonize -p /tmp/loader.pid -c ./ -l /tmp/loader.lock -v -e ./error.out -o ./std.out "$SCRIPTPATH/run_loader.sh"
