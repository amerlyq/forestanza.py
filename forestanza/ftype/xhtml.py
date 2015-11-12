from forestanza import io
from forestanza.syntax import xhtml

EXT = '.xhtml'

TSEC = """
<h3 id="s{index:04d}">{index:04d}</h3>
<p class="origin">
  {origin:s}
</p><p class="phonet">
  : {phonetics:s}
</p><p class="transl">
  ~ {translation:s}
</p><table class="table"><tbody>
{syntable:s}
</tbody></table><br/>
"""

TSYN = """<tr>
<td><span class="origin">{!s:s}</span></td>
<!-- <td><span class="phonet">{!s:s}</span></td> -->
<td>{!s:s}</td>
</tr>\n"""


class Exporter:
    def __init__(self, dom, **kw):
        self.metainfo = kw
        self.template = io.import_template(__file__, 'xhtml.xml')
        self.style = io.import_template(__file__, 'xhtml.css')
        self.sections = []
        self.synxhtml = xhtml.SynGenXHTML(dom)

    def dump(self):
        self.metainfo.update({'css': self.style + ''.join(self.synxhtml.colors()),
                              'sections': ''.join(self.sections)})
        return self.template.format(**self.metainfo)

    def p_section(self, ind, sec):
        self.sections.append(TSEC.format(
            syntable=''.join([TSYN.format(*row) for row in sec.rows]),
            index=ind, origin=self.synxhtml.pygment_origin(sec.origin),
            phonetics=sec.phonetics, translation=sec.translation))
