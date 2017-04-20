#!/usr/bin/env python

import os
import ujson as json

def create_dir(path):
    """ basically mkdir -p """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if os.path.isdir(path):
            pass
        else:
            raise

def get_files(file_path):
    """ returns all files in a given file_path """
    ret = []
    for root, dirs, files in os.walk(file_path):
        for f in files:
            ret.append(os.path.join(root, f))
    return ret

def memoize(f):
    """ memozation implementation for caching function results """
    class memodict(dict):
        __slots__ = ()
        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return memodict().__getitem__

def load_config_file(file_path):
    """ reads a json file and returns a dict obj
        throws an exception if the file is misssing """
    with open(file_path, 'r') as f:
        return json.load(f)
