from forestanza import io

import datetime

EXT = '.fb2'


class Exporter:
    def __init__(self, **kw):
        self.metainfo = kw
        self.template = io.import_template(__file__, 'fb2.xml')
        self.sections = []

    def dump(self):
        today = datetime.date.today()
        self.metainfo.update({'date': today, 'fulldate': today.ctime(),
                              'base64cover': 'No Covering Image',
                              'sections': ''.join(self.sections)})
        return self.template.format(**self.metainfo)

    def p_section(self, ind, sec):
        text = "<section><title><p>{index:04d}</p></title>\n"
        text += "  <p>{origin:s}</p>\n"
        text += "  <p>: {phonetics:s}</p>\n"
        text += "  <p><emphasis>~ {translation:s}</emphasis></p>\n"
        text += "  <empty-line/>\n"
        text += ''.join(["    <p>| {!s:s} |{!s:s}: {!s:s} </p>\n"
                        .format(*row) for row in sec.rows])
        text += "</section>\n"
        self.sections.append(text.format(index=ind, **sec.__dict__))
