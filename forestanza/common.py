
## Maps list chain over dict with default values
KEYDEF = '_'
def dict_resolve(obj, chain, i=0):
    if not isinstance(obj, dict) or i >= len(chain):
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


# WARNING: need Python >= 3.3
def dict_flatten(obj, chain=[]):
    for k, v in sorted(obj.items()):
        if isinstance(v, dict):
            yield from dict_flatten(v, chain + [k])
        else:
            yield (chain + [k], v)


def dict_intersect(obj, mask):
    if not isinstance(obj, dict) or not isinstance(mask, dict):
        return obj
    return {k: v if KEYDEF == k else dict_intersect(v, mask[k])
            for k, v in obj.items()
            if KEYDEF == k or k in mask}
# { k: v['id1'] for k, v in a.items() if 'id1' in v }
