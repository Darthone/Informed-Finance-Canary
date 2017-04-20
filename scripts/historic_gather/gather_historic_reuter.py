#!/usr/bin/env python
import os
import sys
import argparse

from ifc.gather import reuters, rss
from ifc import common

def parse_args():
    parser = argparse.ArgumentParser(description='Downloads all article from Reuters archives between two dates')
    parser.add_argument('-c', "--config", help="Config file to load in via json. Default ./conf.json", default="./conf.json")
    args = parser.parse_args()
    if not os.path.exists(args.config) or not os.path.isfile(args.config):
        raise IOError("Config file missing or not a file: %s", args.config)
    return args

def main():
    args = parse_args()
    config = common.load_config_file(args.config)
    common.create_dir(config["folder"])

    base_path = config["basePath"]
    stock_path = os.path.join(base_path, "stock")
    other_path = os.path.join(base_path, "other")
    bad_path = os.path.join(base_path, "bad")
    error_path = os.path.join(base_path, "error")
    common.create_dir(error_path)
    common.create_dir(bad_path)
    common.create_dir(stock_path)
    common.create_dir(other_path)

    storage_cfg = rss.ArticleStorageConfig(stock_path, other_path, bad_path, error_path)

    # create gatherers
    gather = reuters.RGatherer(config["start"], config["stop"], storage_cfg, config['reuters'],
                               config["folder"], config["numThreads"])
    #Start them
    gather.start()

    #wait for them to finish
    gather.join()

if __name__ == "__main__":
    main()

