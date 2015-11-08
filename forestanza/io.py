from os import makedirs, path as fs


def load_around(around, name):
    path = fs.join(fs.dirname(fs.realpath(around)), name)

    with open(path) as f:
        data = str(f.read())
    return data
