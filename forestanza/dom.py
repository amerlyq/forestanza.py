from forestanza.common import dict_resolve, dict_flatten, getcolumn


# NOTE additional fields in word is not supposed to be included into syntax
# highlighting, but can be used for generating popups in some markups.

class ForestanzaDOM:
    def __init__(self, clrs, lexs):
        self._clrs = clrs
        self._lexs = lexs
        # print(lexs)
        self.clr = {}

    # BUG: Saved from generator -- no saved?
    def data(self):
        for chain, words in dict_flatten(self._lexs):
            cchn, cval = dict_resolve(self._clrs, chain)
            grp = ''.join(cchn)
            if grp not in self.clr:
                self.clr[grp] = cval if isinstance(cval, list) else [cval]
            yield (chain, grp, getcolumn(words, 0), getcolumn(words, 1))

    def colors(self):
        if not self.clr:
            raise SyntaxError()
        return self.clr.items()
