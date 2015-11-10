SYNFMT = "syn match fza_{:s} display '\\v\\c{:s}'\n"
HLFMT = "hi def fza_{:s} {:s}\n"
COPTS = ['ctermfg', 'guifg', 'ctermbg', 'guibg']


class SynGenVim:
    def __init__(self, dom):
        self._dom = dom

    def ddump(self):
        return {'origin': self.make_from(2),
                'phonetic': self.make_from(3),
                'colors': self.colors()}

    def make_from(self, idx):
        for entry in self._dom.data():
            rgx = '|'.join(entry[idx])
            if rgx:
                yield SYNFMT.format(entry[1], rgx)

    def colors(self):
        for grp, clr in sorted(self._dom.colors()):
            opts = ['{:s}={!s:s}'.format(*L) for L in zip(COPTS, clr)]
            yield HLFMT.format(grp, ' '.join(opts))
