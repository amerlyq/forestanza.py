import sys
from os import makedirs, path as fs

import yaml

from forestanza import __appname__

CONFIGDIR = fs.dirname(fs.abspath(sys.argv[0]))
CACHEDIR = fs.join(fs.expanduser('~/.cache'), __appname__)

def expand_pj(path, around=None):
    if isinstance(path, list):
        path = fs.join(*path)
    if not isinstance(path, str):
        return path
    elif path.startswith(":/"):
        return fs.join(CONFIGDIR, path[2:])
    elif path.startswith("@/"):
        if not fs.exists(CACHEDIR):
            makedirs(CACHEDIR)
        return fs.join(CACHEDIR, path[2:])

def import_data(path):
    with open(path) as f:
        data = str(f.read())
    return data

def import_yaml(name):
    path = [':', 'cfg', name + '.yml']
    with open(expand_pj(path)) as f:
        return yaml.safe_load(f)

def load_around(file__, name):
    path = fs.join(fs.dirname(fs.realpath(file__)), name)
    return import_data(path)

def export_cache(name, lines):
    path = ['@', name + '.vim']
    with open(expand_pj(path), 'w') as f:
        f.writelines(lines)

