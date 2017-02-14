#!/usr/bin/env bash
daemonize /home/dario/school/senior-design/bug-free-octo-parakeet/rss_grabber/rss_gather.py -p /tmp/gather.pid -c ./ -l /tmp/gather.lock -v -e ./error.out -o ./std.out
