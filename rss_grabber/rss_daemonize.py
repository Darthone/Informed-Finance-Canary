from time import sleep
from daemonize import Daemonize

pid = "/tmp/test.pid"


def main():
    while True:
        sleep(5)

daemon = Daemonize(app="rss_grabber", pid=pid, action=main)
daemon.start()
