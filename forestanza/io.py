import sys
import types
from os import getenv, makedirs, path as fs

import yaml

from forestanza import __appname__


def _dst_chooser():
    # sdcard = fs.join('/mnt', '0', 'Books')
    # if 'android' == getenv('USER') and fs.isdir(sdcard):
    #     return sdcard
    cache = fs.expanduser('~/.cache')
    if fs.isdir(cache):
        return cache
    return getenv('TMPDIR') or fs.join('/tmp', getenv('USER'))

CONFIGDIR = fs.dirname(fs.abspath(sys.argv[0]))
DSTDIR = fs.join(_dst_chooser(), __appname__)


def clean_cache(name):
    import glob, os
    for f in glob.glob(fs.join(DSTDIR, name + '.*')):
        os.remove(f)


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
        if not fs.exists(DSTDIR):
            makedirs(DSTDIR)
        return fs.join(DSTDIR, path[2:])


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
