
KEYDEF = '_'
def resolve_chain(obj, chain, i=0):
    if not isinstance(obj, dict) or i >= len(chain):
        return chain[:i]  # i -- количество удачно пройденных звеньев
    if chain[i] in obj:
        ret = resolve_chain(obj[chain[i]], chain, i+1)
        if ret is not None:
            return ret
    if KEYDEF in obj:
        return chain[:i] + [KEYDEF]
