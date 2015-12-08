import re

SYNFMT = '<span class="fza {!s:s}">\\1</span>'
RGXFMT = '(?!<span[^<>]*>[^<>]*)({!s:s})(?![^<>]*</span>)'
HLFMT = '.fza.{group:s} {{ color: {guifg:s}; }}\n'
LEGFMT = '<span class="fza {group:s}">{group:s}</span>\n'
COPTS = ['ctermfg', 'guifg', 'ctermbg', 'guibg']


class SynGenXHTML:
    def __init__(self, dom):
        self._dom = dom
        self.origin = list(self.make_from(2))
        self.phonet = list(self.make_from(3))

    # WARNING: can't use dict, as I need fixed order on function calls!
    def pygment_origin(self, text):
        for r, s in self.origin:
            text = r.sub(s, text)
        return text

    def pygment_phonet(self, text):
        for r, s in self.phonet:
            text = r.sub(s, text)
        return text

    def perl_convert(self, rgx):
        rgx = rgx.replace('<', r'\b').replace('>', r'\b').replace('(', r'(?:')
        # NOTE If overlapping is allowed -- by '.' at beg or end -- skip side checking
        # print(rgx)
        return rgx

    def make_from(self, idx):
        for entry in self._dom.data():
            rgx = self.perl_convert('|'.join(entry[idx]))
            if rgx:
                yield (re.compile(RGXFMT.format(rgx)), SYNFMT.format(entry[1]))

    def colors(self):
        for grp, clr in sorted(self._dom.colors()):
            # WARNING: clr[1] -- out index! need dict!
            yield HLFMT.format(group=grp, guifg=clr[1])

    def legend(self):
        for grp, clr in sorted(self._dom.colors()):
            yield LEGFMT.format(group=grp)
