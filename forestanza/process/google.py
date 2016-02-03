import re
import json
from urllib import request
from urllib.parse import urlencode
from subprocess import check_output

from kitchen.text.display import textual_width_fill

from forestanza.io import expand_pj

# AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0"
AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'
REQ_GLETR = '/translate_a/single?client=t&ie=UTF-8&oe=UTF-8&dt=rm&dt=t&dt=at&'
# '&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&' +
EXL_PARTS = ['(aux:relc)', '(null:pronoun)']
REM_WORDS = ['.', '"', '!', '?', u'\u300c', u'\u300d', '(', ')', '.'*6]


class Translator:
    def __init__(self):
        self.host = "translate.google.com"
        self.url = "http://" + self.host

    def _make_req(self, text, sl='ja', tl='en', hl='en'):
        cmd = (expand_pj(':/scripts/tk_hack.pl'), text)
        tk = check_output(cmd).decode('utf-8').rstrip()
        return REQ_GLETR + urlencode([('q', text), ('sl', sl), ('tl', tl),
                                      ('hl', hl), ('tk', tk)])

    def _response(self, line):
        link = self.url + self._make_req(line)
        req = request.Request(url=link, headers={"User-Agent": AGENT})
        data = request.urlopen(req).read().decode('utf-8')
        ## Fill empty array items with 'null' to obtain valid JSON.
        return re.sub(r'(?<=,|\[)(?=,|\])', r'null', data)

    def translate(self, line):
        # lst = wrap(text, 1000, replace_whitespace=False)
        # return ' '.join(self.parse_entry(s) for s in lst)
        # WARNING: we assume, that all lines already manually splitted!
        return self._response(line)


class ResponseParser:
    def __init__(self, rsp):
        self.origin = ""
        self.translation = ""
        self.phonetics = ""
        self.rows = []
        self.parse(rsp)

    def refine_word(self, japword):
        parts = reversed(japword.split())
        parts = filter(lambda x: x not in EXL_PARTS, parts)
        word = ' '.join(parts)
        if not word or word in REM_WORDS:
            return None
        if word in [',']:
            return '-' * 10
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
