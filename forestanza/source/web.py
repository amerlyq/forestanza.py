import os
import re
from urllib import request

from lxml import html


def load(url):
    req = request.urlopen(url)
    return req.read().decode('utf-8')


def refine(path):
    root = html.parse(path).getroot()
    body = root.get_element_by_id("novel_honbun")
    text = re.sub(
        u'(?<=\u3002|\uff01|\uff1f)(?![\x20\u3000]*(?:\u300d|\u300f|\u3002|\uff01|\uff1f|$))',
        u'\n', body.text_content(), flags=re.MULTILINE and re.UNICODE)
    lines = [s.strip(u'\t\x20\u3000') for s in text.splitlines()]
    return os.linesep.join([s for s in lines if s])
