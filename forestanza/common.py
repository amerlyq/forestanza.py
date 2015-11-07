
## Maps list chain over dict with default values
KEYDEF = '_'
def dict_resolve(obj, chain, i=0):
    if not isinstance(obj, dict) or i >= len(chain):
        return chain[:i]  # i -- количество удачно пройденных звеньев
    if chain[i] in obj:
        ret = dict_resolve(obj[chain[i]], chain, i+1)
        if ret is not None:
            return ret
    if KEYDEF in obj:
        return chain[:i] + [KEYDEF]
# THINK could be optimized by moving on next step i -> i+1
# and starting from i=1
# return dict_resolve(obj, chain, i+1)


def dict_intersect(obj, mask):
    pass
#     if not isinstance(obj, dict):
#         return obj
#     return {k: dict_intersect(v, mask[k] if '' != k else )
#             for k, v in obj.items()
#             if '' == k or k in mask}
# { k: v['id1'] for k, v in a.items() if 'id1' in v }

