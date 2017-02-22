#!/usr/bin/env python
import os
import sys
import argparse

import ifc.gather.reuters as reuters
from ifc import common

def parse_args():
    parser = argparse.ArgumentParser(description='Downloads all article from Reuters archives between two dates')
    parser.add_argument('-c', "--config", help="Config file to load in via json. Default ./conf.json", default="./conf.json")
    args = parser.parse_args()
    if not os.path.exists(args.config) or not os.path.isfile(args.config):
        raise IOError("Config file missing or not a file: %s", args.config)
    return args

def main():
    sys.path.append("../")
    args = parse_args()
    config = common.load_config_file(args.config)
    common.create_dir(config["folder"])

    # create gatherers
    gather = reuters.RGatherer(config["start"], config["stop"], config['reuters'],
                               config["folder"], config["numThreads"])
    #Start them
    gather.start()

    #wait for them to finish
    gather.join()

if __name__ == "__main__": 
    main()

