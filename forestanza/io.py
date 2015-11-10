import sys
import types
from os import makedirs, path as fs

import yaml

from forestanza import __appname__

CONFIGDIR = fs.dirname(fs.abspath(sys.argv[0]))
CACHEDIR = fs.join(fs.expanduser('~/.cache'), __appname__)


def expand_pj(path, around=None):
    if not isinstance(path, (list, str)):
        raise ValueError()
    if isinstance(path, list):
        path = fs.join(*path)
    # TODO: split by '/|\\' and join back to uniform?
    if around:
        return fs.join(fs.dirname(fs.realpath(around)), path)
    elif path.startswith(":"):
        return fs.join(CONFIGDIR, path[2:])
    elif path.startswith("@"):
        if not fs.exists(CACHEDIR):
            makedirs(CACHEDIR)
        return fs.join(CACHEDIR, path[2:])


def import_template(file__, name):
    with open(expand_pj(name, around=file__)) as f:
        data = f.read()
    return data


def import_yaml(name):
    with open(expand_pj([':', 'cfg', name + '.yml'])) as f:
        return yaml.safe_load(f)


def export_cache(relpath, data, keep=False):
    path = expand_pj(['@', relpath])
    if keep and fs.exists(path):
        return
    with open(path, 'w') as f:
        if isinstance(data, types.FunctionType):
            data = data()
        if isinstance(data, (list, types.GeneratorType)):
            f.writelines(data)
        elif isinstance(data, str):
            f.write(data)
        else:
            raise TypeError(data)
