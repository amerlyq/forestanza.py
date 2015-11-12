from collections import abc

## Maps list chain over dict with default values
KEYDEF = '_'
def dict_resolve(obj, chain, i=0):
    if not isinstance(obj, abc.Mapping) or i >= len(chain):
        return (chain[:i], obj)
    if chain[i] in obj:
        ret = dict_resolve(obj[chain[i]], chain, i+1)
        if ret is not None:
            return ret
    if KEYDEF in obj:
        return (chain[:i] + [KEYDEF], obj[KEYDEF])
# THINK could be optimized by moving on next step i -> i+1
# and starting from i=1
# return dict_resolve(obj, chain, i+1)
# NEXT optimization through cache resolved partial matches in dict


# WARNING: need Python >= 3.3
# DEV: nested lists for one key-value -- to split lexems logically w/o name.
#   := elif isinstance(obj, list) and isinstance(obj[0], list):
def dict_flatten(obj, chain=[]):
    for k, v in obj.items():
        if isinstance(v, abc.Mapping):
            yield from dict_flatten(v, chain + [k])
        else:
            yield (chain + [k], v)


def getcolumn(obj, idx):
    for e in obj:
        if isinstance(e, abc.Iterable):
            if idx < len(e):
                yield e[idx]
        elif idx == 0:
            yield e


def dict_intersect(obj, mask):
    if (not isinstance(obj, abc.Mapping) or not isinstance(mask, abc.Mapping)):
        return obj
    return {k: v if KEYDEF == k else dict_intersect(v, mask[k])
            for k, v in obj.items()
            if KEYDEF == k or k in mask}
# { k: v['id1'] for k, v in a.items() if 'id1' in v }
