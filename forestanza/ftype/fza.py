EXT = '.fza'


# DEV TODO header for fza '0: > ...' -- move common parts in separate function.
class Exporter:
    def __init__(self, dom, **kw):
        self.metainfo = kw
        self.sections = []
        self.template = ">>> {title:s} ({author:s})\n\n{sections:s}"

    def dump(self):
        self.metainfo.update({'sections': ''.join(self.sections)})
        return self.template.format(**self.metainfo)

    def p_section(self, ind, sec):
        text = "<--{index:04d}-->\n"
        text += "{origin:s}\n: {phonetics:s}\n~ {translation:s}\n"
        text += ''.join(["| {!s:s} |{!s:s}: {!s:s}\n"
                        .format(*row) for row in sec.rows])
        text += '\n'
        self.sections.append(text.format(index=ind, **sec.__dict__))
