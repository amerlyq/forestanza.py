import re

from forestanza import io
from forestanza.syntax import xhtml

EXT = '.xhtml'

TSEC = """
<h3 id="s{index:04d}">{index:04d}</h3>
<p class="origin">\n  {origin:s}\n</p>
<p class="phonet">\n  : {phonetics:s}\n</p>
<p class="transl">\n  ~ {translation:s}\n</p>
<table class="table"><tbody>\n{syntable:s}\n</tbody></table><br/>
"""

TSYN = """<tr>
  <td class="origin">{!s:s}</td>
  <!-- <td class="phonet">{!s:s}</td> -->
  <td>{!s:s}</td>
</tr>\n"""

ESCAPES = (re.compile('&(?!amp;)'), '&amp;')


class Exporter:
    def __init__(self, dom, **kw):
        self.metainfo = kw
        self.template = io.import_template(__file__, 'xhtml.xml')
        self.style = io.import_template(__file__, 'xhtml.css')
        self.script = io.import_template(__file__, 'xhtml.js')
        self.sections = []
        self.synxhtml = xhtml.SynGenXHTML(dom)

    def dump(self):
        self.metainfo.update({'css': self.style + ''.join(self.synxhtml.colors()),
                              'js': self.script,
                              'legend': ''.join(self.synxhtml.legend()),
                              'sections': ''.join(self.sections)})
        r, s = ESCAPES
        return r.sub(s, self.template.format(**self.metainfo))

    def p_section(self, ind, sec):
        syns = [TSYN.format(self.synxhtml.pygment_origin(org.strip()), pho, trl)
                for org, pho, trl in sec.rows]
        self.sections.append(TSEC.format(
            origin=self.synxhtml.pygment_origin(sec.origin),
            phonetics=sec.phonetics,  # self.synxhtml.pygment_phonet(sec.phonetics),
            index=ind, syntable=''.join(syns), translation=sec.translation))
