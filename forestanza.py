#!/usr/bin/env python3

import os
import sys
import re
import json
import datetime
# from textwrap import wrap
from urllib.parse import urlencode
from urllib import request

from lxml import html
from kitchen.text.display import textual_width_fill

import forestanza
from forestanza.ftype import fb2, fza


class FileBundle:
    TMPDIR = os.getenv('TMPDIR') or os.path.join('/tmp', os.getenv('USER'))
    DSTDIR = os.path.join(TMPDIR, forestanza.__appname__)
    EXTENSIONS = ['html', 'src', 'fza', 'fb2', 'xhtml', 'xml', 'req', 'rsp']

    def __init__(self, src, name, chapter):
        self.url = src.format(chapter)
        self.name = name.format(chapter)
        self.make_paths()

    def make_paths(self):
        if not os.path.exists(FileBundle.DSTDIR):
            os.makedirs(FileBundle.DSTDIR)
        dstbase = os.path.join(FileBundle.DSTDIR, self.name)
        for ext in FileBundle.EXTENSIONS:
            setattr(self, ext, dstbase + '.' + ext)


def progress_bar(i, n):
    print("{}/{} = {}%".format(i+1, n, round(100*i/n)))

def get_page(url):
    req = request.urlopen(url)
    return req.read().decode('utf-8')


def extract_content(path):
    root = html.parse(path).getroot()
    body = root.get_element_by_id("novel_honbun")
    text = re.sub(
        u'(?<=\u3002|\uff01|\uff1f)(?![\x20\u3000]*(?:\u300d|\u3002|\uff01|\uff1f))',
        u'\n', body.text_content(), flags=re.MULTILINE and re.UNICODE)
    text = os.linesep.join([s for s in text.splitlines() if s])
    return text


class ResponseParser:
    EXL_PARTS = ['(aux:relc)', '(null:pronoun)']
    REM_WORDS = ['.', '"', '!', '?', u'\u300c', u'\u300d', '(', ')', '.'*6]

    def __init__(self, rsp):
        self.origin = ""
        self.translation = ""
        self.phonetics = ""
        self.rows = []
        self.parse(rsp)

    def refine_word(self, japword):
        parts = reversed(japword.split())
        parts = filter(lambda x: x not in ResponseParser.EXL_PARTS, parts)
        word = ' '.join(parts)
        if not word or word in ResponseParser.REM_WORDS:
            return None
        if word in [',']:
            return '-' * 12
        return word

    def format_row(self, japword, synonyms):
        leftcol = textual_width_fill(japword, 12, left=False)
        synonyms = sorted(synonyms, reverse=True,  # sort in relevance_order:
                          key=lambda x: x[1] if isinstance(x[1], int) else 0)
        rightcol = ', '.join([syn[0] for syn in synonyms])
        phonetics = ""  # DEV: extract from sentence? THINK if possible?
        return [leftcol, phonetics, rightcol]

    def syns_for_parts(self, lexems):
        parts_lst = []
        lex_part = []
        for lex in lexems:
            if lex_part and lex[4] is not None:
                parts_lst.append(lex_part)
                lex_part = []
            lex_part.append(lex)
        parts_lst.append(lex_part)
        return parts_lst

    def parse(self, rsp):
        data = json.loads(rsp)
        try:
            # When origin may contain multiple lines? Right squire bracket used?
            self.translation = ' '.join([str(e[0]) for e in data[0][:-1]])
            self.origin = ' '.join([str(e[1]) for e in data[0][:-1]])
            self.phonetics = str(data[0][-1][3])

            def sorted_as_origin(lexems):
                def origin_order(lex):  # ALT: on-last -- lex[3][-1][-1]
                    return lex[3][0][0] if isinstance(lex[3], list) else 65536
                return sorted(lexems, key=origin_order)

            lexems = sum(map(sorted_as_origin, self.syns_for_parts(data[5])), [])
            self.rows = [self.format_row(self.refine_word(lex[0]), lex[2])
                         for lex in lexems if self.refine_word(lex[0])]
        except TypeError as e:
            print("Err: no such index: " + e)


class GoogleTr:
    AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0"
    def __init__(self):
        self.host = "translate.google.com"
        self.url = "http://" + self.host

    def _make_req(self, text, sl='ja', tl='en', hl='en'):
        return ('/translate_a/single?' + 'client=t&ie=UTF-8&oe=UTF-8' +
                '&dt=rm&dt=t&dt=at&' +
                # '&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&' +
                urlencode([('q', text), ('sl', sl), ('tl', tl), ('hl', hl)]) + '&tk')

    def _response(self, line):
        link = self.url + self._make_req(line)
        req = request.Request(url=link, headers={"User-Agent": GoogleTr.AGENT})
        data = request.urlopen(req).read().decode('utf-8')
        ## Fill empty array items with 'null' to obtain valid JSON.
        return re.sub(r'(?<=,|\[)(?=,|\])', r'null', data)

    def translate(self, line):
        # lst = wrap(text, 1000, replace_whitespace=False)
        # return ' '.join(self.parse_entry(s) for s in lst)
        # WARNING: we assume, that all lines already manually splitted!
        return self._response(line)


if __name__ == '__main__':
    fl = FileBundle('http://ncode.syosetu.com/n8611bv/{:d}',
                    'arifureta-{:d}', 131)

    # Clean cache and all results
    if len(sys.argv) > 1 and sys.argv[1] == '-r':
        for ext in fl.EXTENSIONS:
            if os.path.isfile(getattr(fl, ext)):
                os.remove(getattr(fl, ext))

    # NOTE: save_data() expanded to process get_page/extract only if no cache
    if not os.path.exists(fl.html):
        with open(fl.html, 'w') as f:
            f.write(get_page(fl.url))

    if not os.path.exists(fl.src):
        with open(fl.src, 'w') as f:
            f.write(extract_content(fl.html))

    gt = GoogleTr()
    bCachedRsp = os.path.exists(fl.rsp)
    with open(getattr(fl, 'rsp' if bCachedRsp else 'src'), 'r') as src:
        lst = src.readlines()

    efb2 = fb2.Exporter(author='Xz', title=fl.name)
    efza = fza.Exporter(author='Xz', title=fl.name)

    # Write main body
    with open(fl.fza, 'w') as fza:
        for i, line in enumerate(lst):
            if not bCachedRsp:
                line = gt.translate(line)
                with open(fl.rsp, 'a') as rsp:
                    rsp.write(line + '\n')

            sec = ResponseParser(line)
            efb2.p_section(i+1, sec)
            efza.p_section(i+1, sec)
            progress_bar(i, len(lst))

    # Cover fb2 in header/footer
    with open(fl.fb2, 'w') as f:
        f.write(efb2.dump())
    with open(fl.fza, 'w') as f:
        f.write(efza.dump())
